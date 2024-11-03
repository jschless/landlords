import json
import os
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from model.game import Game
from model.player import Player
from model.hand import Hand
import backend.agent.agent as agent
from typing import List, Dict, Tuple
import random
from faker import Faker

import logging

logger = logging.getLogger(__name__)

fake = Faker()

test_names = ["Tom_U", "Dick_U", "Harry_U"]


class GameController:
    """
    This class will manage the websocket for the game.
    Users will connect, it will communicate with the controller to send messages back and forth
    between server and client
    """

    def __init__(self, game_id: str):
        self.game_id: str = game_id
        self.uid_to_player: Dict[str, int] = {}
        self.active_connections: List[WebSocket] = []
        self.player_to_connection: Dict[int, WebSocket] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.awaiting_from: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, uid: str) -> None:
        logger.info(f"Current connections: {self.active_connections}")
        if len(self.active_connections) > 3:
            logger.info("No more people can join")
        elif uid in self.uid_to_player:
            # don't add a new user, this is a reconnect
            # first check if the existing connection is in active connections and remove
            if (
                self.player_to_connection[self.uid_to_player[uid]]
                in self.active_connections
            ):
                self.active_connections.remove(
                    self.player_to_connection[self.uid_to_player[uid]]
                )

            self.player_to_connection[self.uid_to_player[uid]] = websocket
            logger.info(
                f"{uid} reconnected, switching the player_to_connection mapping {self.player_to_connection}"
            )

            self.active_connections.append(websocket)
            await websocket.accept()
            await self.update_all()

            # Resend message if we were awaiting a response and disconnect took place
            if uid in self.awaiting_from:
                logger.info("Resending message")
                await self.send_personal_message(
                    self.uid_to_player[uid], self.awaiting_from[uid]
                )

        else:
            self.add_player(websocket, None, uid)
            await websocket.accept()
            await self.update_all()

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            logger.info("Disconnecting websocket")
            self.active_connections.remove(websocket)

    def add_player(self, websocket: WebSocket, username: str | None, uid: str) -> None:
        self.player_to_connection[len(self.active_connections)] = websocket
        self.uid_to_player[uid] = len(self.active_connections)
        self.active_connections.append(websocket)
        if username is None:
            if os.getenv("TEST") == "True":
                username = test_names[len(self.g.players)] + f"{self.g.game_count}"
            else:
                username = fake.name()
        self.g.players.append(Player(username=username, uid=uid))

    def player_to_uid(self, player_id: int) -> str:
        for uid, pid in self.uid_to_player.items():
            if pid == player_id:
                return uid

    ### COMMUNICATION FUNCTIONS

    async def wait_for_message(self, player_id: int, msg: Dict) -> Dict:
        """Retrieve a message from the queue for the given player_id."""
        logger.info(
            f"Call to wait_for_message from {player_id} with action {msg['action']}"
        )
        self.awaiting_from[self.player_to_uid(player_id)] = msg
        temp_mapper = {
            "make_a_bid": "bet",
            "make_a_move": "move",
            "game_over": "play_again",
        }
        while True:
            p_id, message_action, message = await self.message_queue.get()
            logger.info(
                f"Wait for message received this {p_id}, {message_action}, {message}"
            )
            if p_id == player_id and message_action == temp_mapper[msg["action"]]:
                del self.awaiting_from[self.player_to_uid(player_id)]
                return message

    async def listen_for_messages(self, websocket: WebSocket, uid: str) -> None:
        player_id = self.uid_to_player[uid]
        try:
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
        except RuntimeError:
            logger.error("ERROR: Likely tried to listen on a broken websocket.")
            self.disconnect(websocket)

    async def send_personal_message(
        self, player_id: int, message: Dict, attempt_number: int = 0
    ) -> None:
        if attempt_number > 30:
            logger.error(
                f"Could not send message {message} to {player_id} over past 30 seconds"
            )
        if message is None:
            return
        if self.player_to_connection[player_id] not in self.active_connections:
            logger.info(
                f"Player {player_id} is not currently connected... trying again in 1 second"
            )
            await asyncio.sleep(1)
            await self.send_personal_message(player_id, message, attempt_number + 1)
            return

        try:
            await self.player_to_connection[player_id].send_text(json.dumps(message))
        except WebSocketDisconnect:
            logger.info(
                f"Disconnect while trying to send a personal message to {player_id} with {message}"
            )
            self.disconnect(self.player_to_connection[player_id])
        except RuntimeError as e:
            logger.info(
                f"EXCEPTION {e}  while trying to send a personal message to {player_id} with {message}"
            )

    async def update_all(self) -> None:
        for player_id, _ in self.player_to_connection.items():
            uid = self.player_to_uid(player_id)
            await self.send_personal_message(player_id, self.g.game_data(uid))

    async def alert_all(self, message) -> None:
        for player_id, _ in self.player_to_connection.items():
            msg = {"action": "alert", "message": message}
            await self.send_personal_message(player_id, msg)

    ### GAME LOGIC CONTROL

    async def try_to_start(self) -> None:
        if (
            len(self.active_connections) == 3
            and self.g.can_start()
            and not self.g.started
        ):
            logger.info("Starting game now!")
            await self.start_game()

    async def game_loop(self) -> None:
        while not self.g.is_over():
            await self.run_round()

        winner = self.g.get_winner()
        self.g.update_scoreboard()
        await self.update_all()

        await self.alert_all(
            f"{winner.username} wins this game! And {self.g.bid*2} points!"
        )

        logger.info(f"Game over. Winner: {winner}.\nScoreboard: {self.g.scoreboard}")

        if os.getenv("SERVER_DEVELOPMENT").lower() == "true":
            # For better control over when the tests start
            if self.g.players[self.g.landlord].robot:
                return
            msg = {"action": "game_over"}
            await self.send_personal_message(self.g.landlord, msg)
            response = await self.wait_for_message(self.g.landlord, msg)
            logger.info(f"Renew game response was {response}")
            if response["decision"]:
                await self.play_again()
        else:
            await self.play_again()

    async def play_again(self) -> None:
        logger.info("Resetting game and starting over.")
        self.g.reset_game()
        await self.start_game()

    def initialize_game(
        self, players: List[Player], game_id: str, game_count: int
    ) -> None:
        self.g = Game(game_id=game_id, players=players)
        self.g.game_count = game_count

    async def start_game(self) -> None:
        if os.getenv("TEST", "false").lower() == "true":
            logger.info("Not shuffling... this is the test environment.")
        elif os.getenv("SERVER_DEVELOPMENT", "false").lower() == "true":
            logger.info(
                "Initializing to stacked hands... this is the test environment."
            )
            self.g.deck = []
            self.g.deck.extend([3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7])
            self.g.deck.extend(
                [7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12]
            )
            self.g.deck.extend(
                [8, 9, 10, 11, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 15]
            )
            self.g.deck.extend([15, 16, 17])
        else:
            self.g.shuffle_deck()

        self.deal_cards()
        self.g.get_blind()
        self.flip_one_card()
        self.g.started = True
        self.g.initialize_scoreboard()

        await self.update_all()
        await self.determine_landlord()

        if self.g.landlord is None:
            raise NotImplementedError("No one became landlord")
        else:
            self.g.players[self.g.landlord].make_landlord(self.g.blind)
            await self.update_all()
            await self.game_loop()

    async def run_round(self) -> None:
        # first turn establishes hand type
        self.g.initialize_round()
        cur_hand, last_player = None, None

        while True:
            new_hand = None
            for i in range(3):
                # need to get the right thing from a player, so give them 3 chances then pass
                try:
                    new_hand, new_player = await self.get_turn(cur_hand)
                    if new_hand is None:
                        self.g.players[new_player].last_move = []
                    else:
                        new_hand_cards = new_hand.kicker_cards + new_hand.hand_cards
                        new_hand_cards.sort()
                        self.g.players[new_player].last_move = new_hand_cards
                    # break for loop if this is valid
                    break
                except ValueError:
                    await self.send_personal_message(
                        self.g.current_player,
                        {
                            "action": "alert",
                            "message": f"That was an improper hand. You need to submit something of type {cur_hand}.<br>{2-i} attempts remaining.",
                        },
                    )
            logger.info(f"The following hand was submitted: {new_hand}, updating")

            self.g.next_player()

            if self.g.is_over():
                logger.info("Exiting run_round loop, round is over")
                return

            if new_hand is not None:
                cur_hand, last_player = new_hand, new_player
                self.g.register_hand(
                    self.g.players[last_player].username, cur_hand.serialize()
                )
            else:
                # This person passed
                self.g.register_hand(
                    self.g.players[(self.g.current_player - 1) % 3].username, None
                )

            if self.g.current_player == last_player:
                # The round is over because the last two people passed
                logger.info(f"{self.g.players[self.g.current_player]} wins the round")
                await self.alert_all(
                    f"{self.g.players[self.g.current_player].username} wins the round"
                )
                self.g.register_round()
                self.g.initialize_round()
                await self.update_all()
                break

            await self.update_all()

    def deal_cards(self) -> None:
        for i in range(3):
            self.g.players[i].deal_cards(sorted(self.g.deck[17 * i : 17 * (i + 1)]))

    def flip_one_card(self) -> None:
        # randomly chose someone to flip a card. they will bid first
        if (
            os.getenv("SERVER_DEVELOPMENT", "false").lower() == "true"
            or os.getenv("TEST", "false").lower() == "true"
        ):
            self.g.current_player = 0
            self.g.players[self.g.current_player].flip_card(index_to_flip=1)
        else:
            self.g.current_player = random.choice([0, 1, 2])
            self.g.players[self.g.current_player].flip_card()

    async def determine_landlord(self) -> None:
        # solicit bids one after the other, needs to be in websocket
        highest_bid, highest_bidder = 0, None
        starting_player = self.g.current_player
        for i in range(3):
            player_id = (starting_player + i) % 3
            self.g.current_player = player_id
            await self.update_all()
            if self.g.players[player_id].robot:
                bid = 3  # random.choice([0] + list(range(max(highest_bid, 1), 4)))
            else:
                logger.info(f"Sending bid solicitation to player {i}")
                msg = {"action": "make_a_bid", "last_bid": highest_bid}
                await self.send_personal_message(player_id, msg)
                bid_json = await self.wait_for_message(player_id, msg)
                bid = int(bid_json["bet"])

            if bid > highest_bid:
                highest_bid = bid
                highest_bidder = player_id
                logger.info(f"New highest bidder is {player_id}")
            if highest_bid == 3:
                # no one else needs to bid anymore
                break
        self.g.landlord = highest_bidder
        self.g.current_player = highest_bidder
        self.g.bid = highest_bid
        logger.info(
            f"Setting landlord as highest_bidder: {highest_bidder}. Bid for round is {self.g.bid}"
        )

    def parse_move(self, json_data: Dict) -> Hand:
        logger.info(f"Trying to parse this JSON as a move: {json_data}")
        return Hand.parse_hand(json_data["cards"], json_data["kickers"])

    def get_prediction(self):
        moves = agent.predict(self.g)
        best_move = agent.extract_best_move(moves)
        hand_cards, kicker_cards = agent.separate_hand_from_kicker(best_move.move)
        hand = Hand.parse_hand(hand_cards, kicker_cards)
        logger.info(f"robot chose {best_move} or {hand}")
        return hand

    async def get_turn(self, h: Hand | None) -> Tuple[Hand, int]:
        # get turn from current_player
        if self.g.players[self.g.current_player].robot:
            new_hand = self.get_prediction()
        else:
            serializable_hand = None if h is None else h.model_dump(mode="json")
            possible_moves = Hand.suggest_moves(
                h, self.g.players[self.g.current_player].cards
            )
            msg = {
                "action": "make_a_move",
                "last_hand": serializable_hand,
                "possible_moves": possible_moves[:5],
            }
            logger.info(f"Soliciting move from {self.g.current_player}")
            await self.send_personal_message(self.g.current_player, msg)
            new_hand_json = await self.wait_for_message(self.g.current_player, msg)
            new_hand = self.parse_move(new_hand_json)
            logger.info(f"Parsed move of {new_hand}")

            # Check if cards are in hand
            if not self.g.players[self.g.current_player].has_cards(new_hand):
                logger.info(
                    f"{self.g.current_player} tried to play cards they didn't have"
                )
                raise ValueError("Player doesn't have the cards")

        # Move has been validated, check if it works.
        cur_player = self.g.current_player

        if new_hand is None:
            # Player submitted a pass
            return None, cur_player
        elif h is None or h.is_valid_successor(new_hand):
            # Player submitted a valid hand and there was no round type defined,
            # or they followed a move and it was a valid hand

            logger.info(f"New hand is {new_hand}, old hand was {h}")
            # remove cards
            if new_hand.is_bomb():
                self.g.play_bomb()
                logger.info(f"Bomb was dropped, bid is now {self.g.bid}")

            self.g.players[self.g.current_player].remove_cards(
                new_hand.hand_cards + new_hand.kicker_cards
            )

            await self.update_all()
            return new_hand, cur_player
        else:
            logger.info(f"{new_hand}  was not a valid move with existing hand {h}")
            raise ValueError("Not a valid move")
