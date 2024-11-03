from .player import Player
from .hand import Hand

from typing import List, Optional, Dict, Tuple
from pydantic import BaseModel
import random
import logging

logger = logging.getLogger(__name__)


class Game(BaseModel):
    game_id: str
    players: List[Player]
    current_player: int = 0
    rand_seed: Optional[int] = None
    landlord: Optional[int] = None
    bid: int = 0
    blind: Optional[List[int]] = None
    deck: List[int] = list(range(3, 16)) * 4 + [16, 17]
    rounds: List[List[Tuple[str, Hand] | Tuple[str, None]]] = []
    cur_round: List[Tuple[str, Hand] | Tuple[str, None]] = []
    started: bool = False
    scoreboard: Dict = {}
    game_count: int = 0
    n_bombs_played: int = 0

    def random_gen(self):
        if self.rand_seed:
            return random.Random(self.rand_seed)
        else:
            return random.Random()

    def shuffle_deck(self):
        self.random_gen().shuffle(self.deck)

    def determine_landlord(self) -> Optional[int]:
        # Runs bids and returns index of landlord
        current_bid, current_bidder = 0, None
        for i in range(3):
            current_bid = self.players[i].get_bid(current_bid)
            if current_bid > 0:
                current_bidder = i
            if current_bid == 3:
                return current_bidder
        return current_bidder

    def get_blind(self):
        self.blind = sorted(self.deck[51:])

    def get_winner(self):
        for p in self.players:
            if len(p.cards) == 0:
                return p
        return None

    def is_over(self):
        return any(len(self.players[i].cards) == 0 for i in range(3))

    def can_start(self):
        return len(self.players) == 3

    def next_player(self):
        self.current_player = (self.current_player + 1) % 3

    def initialize_round(self):
        self.cur_round = []

    def register_hand(self, p: Player, h: Hand):
        self.cur_round.append((p, h))

    def register_round(self):
        self.rounds.append(self.cur_round)

    def reset_game(self):
        # Runs after a game is over
        for p in self.players:
            p.reset()
        self.current_player = 0
        self.landlord = None
        self.bid = 0
        self.blind = None
        self.deck = list(range(3, 16)) * 4 + [16, 17]
        self.started = False

    def play_bomb(self):
        self.bid *= 2
        self.n_bombs_played += 1

    def initialize_scoreboard(self):
        if len(self.scoreboard) == 0:
            for p in self.players:
                self.scoreboard[p.username] = 0

    def update_scoreboard(self):
        winner = self.get_winner()
        for p in self.players:
            if p.username == winner.username:
                self.scoreboard[p.username] += 2 * self.bid
            else:
                self.scoreboard[p.username] -= self.bid

    def game_data(self, uid: int):
        new_players = []
        cards = []
        username = ""
        for p in self.players:
            if p.uid != uid:
                new_players.append(
                    {
                        "username": p.username,
                        "n_cards": len(p.cards),
                        "exposed_cards": p.exposed_cards,
                    }
                )
            else:
                cards = p.cards
                username = p.username

        new_dict = {
            "game_id": self.game_id,
            "username": username,
            "my_cards": cards,
            "players": new_players,
            "landlord": self.landlord,
            "landlord_username": None
            if self.landlord is None
            else self.players[self.landlord].username,
            "started": self.started,
            "action": "update",
            "current_player": self.current_player,
            "current_player_username": None
            if len(self.players) < 3
            else self.players[self.current_player].username,
            "current_player_uid": None
            if len(self.players) < 3
            else self.players[self.current_player].uid,
            "scoreboard": self.scoreboard,
            "cur_round": self.cur_round,
            "round_history": self.rounds,
            "bid": self.bid,
        }

        return new_dict
