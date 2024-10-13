import httpx
import asyncio
import json
import websockets


def format_move(cards, kickers):
    return {
        "action": "move",
        "cards": [{"card": c} for c in cards],
        "kickers": [{"card": c} for c in kickers],
    }


async def execute_moves_multiple(fastapi_server, moves):
    # open as many games as necessary
    async def connect_websocket(game_id, user_id, messages_to_send, delay):
        await asyncio.sleep(delay)
        async with websockets.connect(
            f"ws://localhost:8000/ws/game/{game_id}?id={user_id}"
        ) as websocket:
            update = None
            while True:
                try:
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

    game_ids = []
    for i, _ in enumerate(moves):
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/create_game")
            assert response.status_code == 200
            game_ids.append((i, response.json()["game_id"]))

    tasks = []
    for (i, game_id), (p1, p2, p3) in zip(game_ids, moves):
        tasks += [
            connect_websocket(game_id, f"Tom_{i}", p1[::-1], 0),
            connect_websocket(game_id, f"Dick_{i}", p2[::-1], 1),
            connect_websocket(game_id, f"Harry_{i}", p3[::-1], 2),
        ]
    results = await asyncio.gather(*tasks)
    return results
