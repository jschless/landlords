import websockets
import os
from backend.server import app
import pytest
import json
import asyncio
import httpx
import uvicorn
import multiprocessing


def format_move(cards, kickers):
    ans = {"action": "move"}
    card_list = []
    for c in cards:
        card_list.append({"card": c})
    kicker_list = []
    for c in kickers:
        kicker_list.append({"card": c})
    ans["cards"] = card_list
    ans["kickers"] = kicker_list
    return ans


def run_server():
    os.environ["TEST"] = "True"
    uvicorn.run(app, host="127.0.0.1", port=8000)


@pytest.fixture(scope="module")
def fastapi_server():
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()

    asyncio.run(asyncio.sleep(1))

    yield  # This is where the tests will run

    server_process.terminate()
    server_process.join()


async def execute_moves(fastapi_server, p1_moves, p2_moves, p3_moves):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8000/create_game")
        assert response.status_code == 200
        game_id = response.json()["game_id"]

        async def connect_websocket(user_id, messages_to_send, delay):
            await asyncio.sleep(delay)
            async with websockets.connect(
                f"ws://localhost:8000/ws/game/{game_id}?id={user_id}"
            ) as websocket:
                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=5)
                        data = json.loads(message)
                        if (
                            data["action"] == "make_a_bid"
                            or data["action"] == "make_a_move"
                        ):
                            response = messages_to_send.pop()
                            await websocket.send(json.dumps(response))
                        elif data["action"] == "update":
                            update = data
                    except asyncio.TimeoutError:
                        return update
                    except Exception as e:
                        return update

        tasks = [
            connect_websocket("Tom", p1_moves[::-1], 0),
            connect_websocket("Dick", p2_moves[::-1], 1),
            connect_websocket("Harry", p3_moves[::-1], 2),
        ]
        results = await asyncio.gather(*tasks)
        return results


@pytest.mark.asyncio
async def test_through_bet(fastapi_server):
    p1_moves = [{"action": "bet", "bet": "1"}]
    p2_moves = [{"action": "bet", "bet": "2"}]
    p3_moves = [{"action": "bet", "bet": "3"}]

    results = await execute_moves(fastapi_server, p1_moves, p2_moves, p3_moves)
    harry = next((x for x in results if x["username"] == "Harry_U"), None)

    assert harry["landlord"] == 2
    assert len(harry["my_cards"]) == 20


@pytest.mark.asyncio
async def test_through_first_move(fastapi_server):
    p1_moves = [
        {"action": "bet", "bet": "3"},
        {"action": "move", "cards": [{"card": 3}, {"card": 3}], "kickers": []},
    ]
    p2_moves = [
        {"action": "move", "cards": [{"card": 7}, {"card": 7}], "kickers": []},
    ]
    p3_moves = [
        {"action": "move", "cards": [{"card": 11}, {"card": 11}], "kickers": []},
    ]

    results = await execute_moves(fastapi_server, p1_moves, p2_moves, p3_moves)
    tom = next((x for x in results if x["username"] == "Tom_U"), None)
    assert tom["my_cards"].count(3) == 0
    assert len(tom["my_cards"]) == 18
    for p in tom["players"]:
        if p["username"] == "Harry_U":
            # Landlord has played two cards (20 - 18)
            assert p["n_cards"] == 15
        else:
            assert p["n_cards"] == 15


@pytest.mark.asyncio
async def test_complete_hand(fastapi_server):
    """
    P3 wins the round of betting.
    P3 opens with a 6 card straight.
    P1 wins with a better hand.
    Everyone passes until P1 wins
    """
    p1_moves = [
        {"action": "bet", "bet": "1"},
        format_move([6, 7, 8, 9, 10, 11], []),
    ]
    p2_moves = [{"action": "bet", "bet": "2"}, format_move([], [])]
    p3_moves = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8], []),
        format_move([], []),
    ]

    results = await execute_moves(fastapi_server, p1_moves, p2_moves, p3_moves)
    tom = next((x for x in results if x["username"] == "Tom_U"), None)
    assert len(tom["my_cards"]) == 11
    assert tom["current_player"] == 0


@pytest.mark.asyncio
async def test_complete_round(fastapi_server):
    p1_moves = [
        {"action": "bet", "bet": "1"},
        format_move([], []),
        format_move([], []),
    ]
    p2_moves = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ]
    p3_moves = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], []),
        format_move([11, 12, 13, 14, 15], []),
        format_move([16, 17], []),
    ]

    results = await execute_moves(fastapi_server, p1_moves, p2_moves, p3_moves)
    harry = next((x for x in results if x["username"] == "Harry_U"), None)
    assert len(harry["my_cards"]) == 0
    tom = next((x for x in results if x["username"] == "Tom_U"), None)
    assert len(tom["my_cards"]) == 17
