import multiprocessing
import asyncio
import pytest
import uvicorn
from backend.server import app
import os
from .utils import format_move


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


@pytest.fixture(scope="module")
def complete_game_p3_blowout():
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
    return (p1, p2, p3)


@pytest.fixture(scope="module")
def complete_game_p1_blowout():
    p1 = [
        {"action": "bet", "bet": "3"},
        format_move([7, 8, 9, 10, 11, 12, 13, 14], []),
        format_move([3, 3], []),
        format_move([4, 4], []),
        format_move([5, 5], []),
        format_move([6, 6], []),
        format_move([15, 15], []),
        format_move([16, 17], []),
    ]
    p2 = [
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
        format_move([], []),
    ]
    return (p1, p2, p3)
