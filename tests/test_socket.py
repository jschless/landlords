import os
import websockets
from backend.server import app
from fastapi.testclient import TestClient
import pytest
import json
import random
import string
import asyncio
import httpx
import uvicorn
import multiprocessing


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_endpoint_root(client):
    response = client.get("/")
    assert response.status_code == 200


def get_uid():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(8))


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


@pytest.mark.asyncio
async def test_websocket_connections(fastapi_server):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8000/create_game")
        assert response.status_code == 200
        game_id = response.json()["game_id"]

        async def connect_websocket(user_id, messages_to_send=[]):
            async with websockets.connect(
                f"ws://localhost:8000/ws/game/{game_id}?id={user_id}"
            ) as websocket:
                update = None
                # Keep the connection open and stop on timeout
                # TODO: figure out how to exit gracefully at any point for testing purposes
                #
                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=10)
                        data = json.loads(message)
                        if data["action"] == "make_a_bid":
                            response = messages_to_send.pop()
                            await websocket.send(json.dumps(response))
                        elif data["action"] == "update":
                            update = data
                    except asyncio.TimeoutError:
                        return update
                    except Exception as e:
                        return update

        p1_moves = [{"action": "bet", "bet": "1"}]
        p2_moves = [{"action": "bet", "bet": "2"}]
        p3_moves = [{"action": "bet", "bet": "3"}]

        tasks = []
        tasks.append(connect_websocket("Tom", p1_moves))
        await asyncio.sleep(2)
        tasks.append(connect_websocket("Dick", p2_moves))
        await asyncio.sleep(2)
        tasks.append(connect_websocket("Harry", p3_moves))
        results = await asyncio.gather(*tasks)
        harry = next((x for x in results if x["username"] == "Harry_U"), None)

        assert harry["landlord"] == 2
        assert len(harry["my_cards"]) == 20
