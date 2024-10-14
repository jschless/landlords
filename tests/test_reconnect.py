import httpx
import pytest
import asyncio
import websockets
import json
from .conftest import complete_game_p1_blowout, complete_game_p3_blowout


@pytest.mark.parametrize("player_to_test", [0, 1, 2])
@pytest.mark.parametrize("disconnect_round", [0, 1, 2, 3])
@pytest.mark.asyncio
async def test_disconnect(fastapi_server, player_to_test, disconnect_round):
    # open as many games as necessary
    async def connect_websocket(
        game_id, user_id, messages_to_send, delay, reconnect_at_message: int
    ):
        await asyncio.sleep(delay)
        async with websockets.connect(
            f"ws://localhost:8000/ws/game/{game_id}?id={user_id}"
        ) as websocket:
            update = None
            while True:
                try:
                    if reconnect_at_message == len(messages_to_send):
                        break
                    message = await asyncio.wait_for(websocket.recv(), timeout=2)
                    data = json.loads(message)
                    if data["action"] in {
                        "make_a_bid",
                        "make_a_move",
                        "game_over",
                    }:
                        response = messages_to_send.pop()
                        await websocket.send(json.dumps(response))
                    elif data["action"] == "update":
                        update = data

                except asyncio.TimeoutError:
                    return update
                except Exception as e:
                    return update

        if reconnect_at_message == len(messages_to_send):
            return await connect_websocket(game_id, user_id, messages_to_send, 0, -1)

    game_id = None
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/create_game")
        assert response.status_code == 200
        game_id = response.json()["game_id"]

    p1, p2, p3 = complete_game_p3_blowout()

    tasks = []
    i = 0

    tom_var = len(p1) - disconnect_round if 0 == player_to_test else -1
    dick_var = len(p2) - disconnect_round if 1 == player_to_test else -1
    harry_var = len(p3) - disconnect_round if 2 == player_to_test else -1

    tasks += [
        connect_websocket(game_id, f"Tom_{i}", p1[::-1], 0, tom_var),
        connect_websocket(game_id, f"Dick_{i}", p2[::-1], 1, dick_var),
        connect_websocket(game_id, f"Harry_{i}", p3[::-1], 2, harry_var),
    ]
    results = await asyncio.gather(*tasks)
    tom, dick, harry = tuple(results)

    assert len(tom["my_cards"]) == 17
    assert len(harry["my_cards"]) == 0
    assert dick["scoreboard"][harry["username"]] == 12
    assert tom["scoreboard"][dick["username"]] == -6
