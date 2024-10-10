import json
import os
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from model.game import Game
from model.player import Player
from model.hand import Hand
from typing import List, Dict, Set
import random
from faker import Faker

import logging

logger = logging.getLogger(__name__)

fake = Faker()
test_names = [
    "a",
    "x",
    "c",
    "d",
    "g",
    "Harry_U",
    "Dick_U",
    "Tom_U",
]


class GameController:
    """
    This class will manage the websocket for the game.
    Users will connect, it will communicate with the controller to send messages back and forth
    between server and client
    """

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.uid_to_player: Dict[str, int] = {}
        self.active_connections: List[WebSocket] = []
        self.player_to_connection: Dict[int, WebSocket] = {}
        self.message_queue = asyncio.Queue()

    async def connect(self, websocket: WebSocket, uid: str):
        logger.info(f"Current connections: {self.active_connections}")
        if len(self.active_connections) > 3:
            logger.info(f"No more people can join")
            return
        elif uid in self.uid_to_player:
            # don't add a new user, this is a reconnect
            self.player_to_connection[self.uid_to_player[uid]] = websocket
            logger.info(
                f"{uid} reconnected, switching the player_to_connection mapping {self.player_to_connection}"
            )
            self.active_connections.append(websocket)
            await websocket.accept()
        else:
            self.add_player(websocket, None, uid)
            await websocket.accept()

    def add_player(self, websocket: WebSocket, username: str | None, uid: str):
        self.player_to_connection[len(self.active_connections)] = websocket
        self.uid_to_player[uid] = len(self.active_connections)
        self.active_connections.append(websocket)
        if username is None:
            if os.getenv("TEST") == "True":
                username = test_names.pop()
            else:
                username = fake.name()
        self.g.players.append(Player(username=username, uid=uid))

    def player_to_uid(self, player_id: int):
        logger.info(f"uid_to_player: {self.uid_to_player}")
        for uid, pid in self.uid_to_player.items():
            if pid == player_id:
                return uid

    async def wait_for_message(self, player_id: int, action: str):
        """Retrieve a message from the queue for the given player_id."""
        logger.info(f"Call to wait_for_message from {player_id} with action {action}")
        while True:
            p_id, message_action, message = await self.message_queue.get()
            logger.info(
                f"Wait for message received this {p_id}, {message_action}, {message}"
            )
            if p_id == player_id and message_action == action:
                return message

    async def try_to_start(self):
        if len(self.active_connections) == 3 and not self.g.started:
            logger.info("Starting game now!")
            await self.start_game()

    async def listen_for_messages(self, websocket, uid):
        player_id = self.uid_to_player[uid]
        try:
            await self.update(player_id)
            logger.info(f"Persistent listener initiated for {player_id}")
            while True:
                message = await websocket.receive_text()
                message_json = json.loads(message)
                logger.info(
                    f"Server received this message from player {player_id}: {message}"
                )
                await self.message_queue.put(
                    (player_id, message_json["action"], message_json)
                )
        except WebSocketDisconnect:
            logger.info(f"Disconnect while listening for messages for {player_id}")
            self.disconnect(websocket)

    def disconnect(self, websocket: WebSocket):
        logger.info(f"Disconnecting websocket")
        self.active_connections.remove(websocket)

    async def send_personal_message(self, player: int, message: Dict):
        await self.player_to_connection[player].send_text(json.dumps(message))

    async def broadcast(self, message):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)
                logger.info(f"WebSocketDisconnect error in broadcast")

    async def game_loop(self):
        while not self.g.is_over():
            await self.run_round()

    async def update_all(self):
        for player_id, connection in self.player_to_connection.items():
            await self.update(player_id)

    async def update(self, player_id: int):
        # refresh the game state for a certain player
        conn = self.player_to_connection[player_id]
        uid = self.player_to_uid(player_id)
        data = json.dumps(self.g.game_data(uid))
        try:
            logger.info(f"Sending {data} to {uid}/{player_id}")
            await conn.send_text(data)
        except WebSocketDisconnect:
            self.disconnect(conn)

    async def run_round(self):
        # first turn establishes hand type
        cur_round = []
        cur_hand, last_player = None, None
        cur_round.append(cur_hand)
        while True:
            for _ in range(3):
                # need to get the right thing from a player, so give them 3 chances then pass
                try:
                    new_hand, new_player = await self.get_turn(cur_hand)
                except ValueError:
                    logger.info("Submission was malformed or something, try again")

            if new_hand is not None:
                last_hand, last_player = new_hand, new_player
                cur_round.append(last_hand)

            if self.g.current_player == last_player:
                # everyone passed and its back to the starter
                logger.info(f"{self.g.players[self.g.current_player]} wins the round")
                self.g.register_round(cur_round)
                break

    def initialize_game(self, players: List[Player], game_id: str):
        self.g = Game(game_id=game_id, players=players)

    async def start_game(self):
        if not self.g.can_start():
            raise ValueError("Need 3 players to start game")
        if os.getenv("TEST") == "True":
            logger.info("Not shuffling... this is the test environment.")
        else:
            self.g.shuffle_deck()

        self.deal_cards()

        self.g.get_blind()

        self.flip_one_card()

        self.g.started = True

        await self.update_all()

        await self.determine_landlord()

        if self.g.landlord is None:
            raise NotImplementedError("No one became landlord")
        else:
            self.g.players[self.g.landlord].make_landlord(self.g.blind)
            await self.update_all()
            await self.game_loop()

    def deal_cards(self):
        for i in range(3):
            self.g.players[i].deal_cards(sorted(self.g.deck[17 * i : 17 * (i + 1)]))

    def flip_one_card(self):
        # randomly chose someone to flip a card. they will bid first
        if os.getenv("TEST") == "True":
            self.g.current_player = 0
            self.g.players[self.g.current_player].flip_card(index_to_flip=1)
        else:
            self.g.current_player = random.choice([0, 1, 2])
            self.g.players[self.g.current_player].flip_card()

    async def determine_landlord(self):
        # solicit bids one after the other, needs to be in websocket
        highest_bid, highest_bidder = 0, None
        for i in range(3):
            player_id = (self.g.current_player + i) % 3
            logger.info(f"Sending bid solicitation to player {i}")
            await self.send_personal_message(
                player_id,
                {"action": "make_a_bid", "last_bid": highest_bid},
            )
            bid_json = await self.wait_for_message(player_id, "bet")
            bid = int(bid_json["bet"])

            if bid > highest_bid:
                highest_bid = bid
                highest_bidder = player_id
                logger.info(f"New highest bidder is {player_id}")
            if highest_bid == 3:
                break
        logger.info(f"Setting landlord as highest_bidder: {highest_bidder}")
        self.g.landlord = highest_bidder

    def parse_move(self, json_data):
        hand_cards, kicker_cards = [], []
        for c in json_data["cards"]:
            hand_cards.append(c["card"])

        for c in json_data["kickers"]:
            kicker_cards.append(c["card"])

        return Hand.parse_hand(hand_cards, kicker_cards)

    async def get_turn(self, h: Hand | None):
        # get turn from current_player
        await self.send_personal_message(
            self.g.current_player, {"action": "make_a_move", "last_hand": h}
        )
        new_hand_json = await self.wait_for_message(self.g.current_player, "move")
        new_hand = self.parse_move(new_hand_json)
        logger.info(f"Parsed move of {new_hand}")
        # Move has been validated, check if it works.

        if h is None or h.is_valid_successor(new_hand):
            # remove cards
            self.g.players[self.g.current_player].remove_cards(
                new_hand.hand_cards + new_hand.kicker_cards
            )
            await self.update_all()
            g.next_player()
            #
            return hand
        else:
            raise ValueError("Not a valid move")
