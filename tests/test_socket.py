import websockets
import os
from backend.server import app
import pytest
import json
import asyncio
import httpx
import uvicorn
import multiprocessing
from typing import List, Tuple


def format_move(cards, kickers):
    return {
        "action": "move",
        "cards": [{"card": c} for c in cards],
        "kickers": [{"card": c} for c in kickers],
    }


def run_server():
    os.environ["TEST"] = "True"
    uvicorn.run(app, host="127.0.0.1", port=8000)


@pytest.fixture(scope="module")
def fastapi_server():
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()
    asyncio.run(asyncio.sleep(1))
    # This is where the tests will run
    yield
    server_process.terminate()
    server_process.join()


async def execute_moves(fastapi_server, p1_moves, p2, p3):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8000/create_game")
        assert response.status_code == 200
        game_id = response.json()["game_id"]

    async def connect_websocket(user_id, messages_to_send, delay):
        await asyncio.sleep(delay)
        update = None
        async with websockets.connect(
            f"ws://localhost:8000/ws/game/{game_id}?id={user_id}"
        ) as websocket:
            while True:  # len(messages_to_send) > 0:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5)
                    data = json.loads(message)
                    if data["action"] in {
                        "make_a_bid",
                        "make_a_move",
                        "game_over",
                    }:
                        if len(messages_to_send) > 0:
                            response = messages_to_send.pop()
                            await websocket.send(json.dumps(response))
                    elif data["action"] == "update":
                        update = data

                except asyncio.TimeoutError:
                    return update
            return update

    tasks = [
        connect_websocket("Tom", p1_moves[::-1], 0),
        connect_websocket("Dick", p2[::-1], 1),
        connect_websocket("Harry", p3[::-1], 2),
    ]
    results = await asyncio.gather(*tasks)
    return results


@pytest.mark.asyncio
async def test_through_bet(fastapi_server):
    p1 = [{"action": "bet", "bet": "1"}]
    p2 = [{"action": "bet", "bet": "2"}]
    p3 = [{"action": "bet", "bet": "3"}]

    results = await execute_moves(fastapi_server, p1, p2, p3)
    tom, dick, harry = tuple(results)

    assert harry["landlord"] == 2
    assert len(harry["my_cards"]) == 20


@pytest.mark.asyncio
async def test_through_first_move(fastapi_server):
    p1 = [{"action": "bet", "bet": "3"}, format_move([3, 3], [])]
    p2 = [format_move([7, 7], [])]
    p3 = [format_move([11, 11], [])]

    results = await execute_moves(fastapi_server, p1, p2, p3)

    tom, dick, harry = tuple(results)

    assert tom["my_cards"].count(3) == 0
    assert len(tom["my_cards"]) == 18
    for p in tom["players"]:
        if p["username"] == harry["username"]:
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
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([6, 7, 8, 9, 10, 11], []),
    ]
    p2 = [{"action": "bet", "bet": "2"}, format_move([], [])]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8], []),
        format_move([], []),
    ]

    results = await execute_moves(fastapi_server, p1, p2, p3)

    tom, dick, harry = tuple(results)
    assert len(tom["my_cards"]) == 11
    assert tom["current_player"] == 0


@pytest.mark.asyncio
async def test_complete_round(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([], []),
        format_move([], []),
    ]
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], []),
        format_move([11, 12, 13, 14, 15], []),
        format_move([16, 17], []),
    ]

    results = await execute_moves(fastapi_server, p1, p2, p3)

    tom, dick, harry = tuple(results)

    assert len(harry["my_cards"]) == 0
    assert len(tom["my_cards"]) == 17

    assert harry["scoreboard"][harry["username"]] == 12


@pytest.mark.asyncio
async def test_two_rounds(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([], []),
        format_move([], []),
    ] * 2
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ] * 2
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], []),
        format_move([11, 12, 13, 14, 15], []),
        format_move([16, 17], []),
        {"action": "play_again", "decision": True},
    ] * 2

    results = await execute_moves(fastapi_server, p1, p2, p3)
    tom, dick, harry = tuple(results)
    assert harry["scoreboard"][harry["username"]] == 24
    # assert len(harry["my_cards"]) == 0
    # tom = next((x for x in results if x["username"] == "Tom_U"), None)
    # assert len(tom["my_cards"]) == 17


@pytest.mark.asyncio
async def test_invalid_start_move(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([6, 7, 8, 9, 10], []),
        format_move([], []),
    ]
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 5, 6, 7, 8], []),  # bad move
        format_move([3, 4, 5, 6, 7], []),  # correct move
        format_move([], []),
    ]

    results = await execute_moves(fastapi_server, p1, p2, p3)

    # So Tom should be current_play

    tom, dick, harry = tuple(results)
    assert tom["current_player"] == 0
    assert len(harry["my_cards"]) == 15
    assert len(tom["my_cards"]) == 12
    assert len(dick["my_cards"]) == 17


@pytest.mark.asyncio
async def test_invalid_following_move(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([6, 7, 8, 9, 10, 11], []),
        format_move([], []),
    ]
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 5, 6, 7, 8], []),  # bad move
        format_move([3, 4, 5, 6, 7], []),  # correct move
        format_move([], []),
    ]

    results = await execute_moves(fastapi_server, p1, p2, p3)

    tom, dick, harry = tuple(results)
    assert tom["current_player"] == 2

    assert len(harry["my_cards"]) == 15
    assert len(tom["my_cards"]) == 17
    assert len(dick["my_cards"]) == 17


@pytest.mark.asyncio
async def test_simultaneous_connections():
    pass


@pytest.mark.asyncio
async def test_beginning_disconnect():
    pass


@pytest.mark.asyncio
async def test_midround_disconnect():
    pass
