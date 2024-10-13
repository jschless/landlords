import multiprocessing
import asyncio
import pytest
import uvicorn
from backend.server import app
import os


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
