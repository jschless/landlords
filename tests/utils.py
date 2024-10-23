import httpx
import asyncio
import json
import websockets
from datetime import datetime


def format_move(cards, kickers):
    return {"action": "move", "cards": cards, "kickers": kickers}


async def execute_moves_multiple(
    fastapi_server, moves, player_to_test=-1, disconnect_round=-1
):
    # open as many games as necessary
    async def connect_websocket(
        game_id, user_id, messages_to_send, delay, reconnect_at_message=-1
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
                    message = await asyncio.wait_for(websocket.recv(), timeout=5)
                    print(f"{user_id}: Received {message}")
                    data = json.loads(message)
                    if data["action"] in {
                        "make_a_bid",
                        "make_a_move",
                        "game_over",
                    }:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
                        print(
                            f"{timestamp} - {user_id}: received call for {message}\nMessage queue is {messages_to_send}"
                        )

                        response = messages_to_send.pop()
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
                        print(f"{timestamp} - {user_id} sending {response}")
                        await websocket.send(json.dumps(response))
                    elif data["action"] == "update":
                        update = data

                except asyncio.TimeoutError:
                    return update
                except Exception:
                    return update
        if reconnect_at_message == len(messages_to_send):
            await asyncio.sleep(3)
            return await connect_websocket(game_id, user_id, messages_to_send, 0, -1)

    game_ids = []
    for i, _ in enumerate(moves):
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/create_game")
            assert response.status_code == 200
            game_ids.append((i, response.json()["game_id"]))

    tasks = []
    for (i, game_id), (p1, p2, p3) in zip(game_ids, moves):
        tom_var = len(p1) - disconnect_round if 0 == player_to_test else -1
        dick_var = len(p2) - disconnect_round if 1 == player_to_test else -1
        harry_var = len(p3) - disconnect_round if 2 == player_to_test else -1

        tasks += [
            connect_websocket(game_id, f"Tom_{i}", p1[::-1], 0, tom_var),
            connect_websocket(game_id, f"Dick_{i}", p2[::-1], 1, dick_var),
            connect_websocket(game_id, f"Harry_{i}", p3[::-1], 2, harry_var),
        ]
    results = await asyncio.gather(*tasks)
    return results
