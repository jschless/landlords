import random
import string

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import asyncio

from backend.game_controller import GameController
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["http://localhost:3000", "http://134.122.123.229:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows CORS for the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

games = {}


def gen_game_id(length=5):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


@app.get("/")
async def get_home():
    return HTMLResponse("<h1>Welcome to the game</h1>")


@app.post("/create_game")
async def create_game():
    game_id = gen_game_id()
    game_manager = GameController(game_id)
    game_manager.initialize_game(players=[], game_id=game_id, game_count=len(games))
    games[game_id] = game_manager
    return {"game_id": game_id}


@app.get("/game/{game_id}")
async def game_lobby(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    return games[game_id].g.game_data(None)


@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    user_id = websocket.query_params.get("id")
    if not user_id:
        await websocket.close(code=1008)
        logger.info("Closing connection to websocket, no user_id provided")
        return

    await games[game_id].connect(websocket, user_id)

    listen_task = asyncio.create_task(
        games[game_id].listen_for_messages(websocket, user_id),
        name=f"Listener for {user_id}",
    )
    logger.info(f"Backgrounding listen task for {user_id}")

    if not games[game_id].g.started:
        asyncio.create_task(
            games[game_id].try_to_start(),
            name=f"Attempting to start after {user_id} joins",
        )
        logger.info(f"Backgrounding try_to_start task for {user_id}")

    await listen_task

    logger.info(f"Finally awaited listen_task for {user_id}")
