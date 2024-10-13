from model.hand import Hand
from pydantic import BaseModel, Field
from typing import List
from collections import Counter
import random


class Player(BaseModel):
    username: str
    uid: str
    cards: List[int] = Field(default_factory=list)
    exposed_cards: List[int] = Field(default_factory=list)
    spent_cards: List[int] = Field(default_factory=list)

    def deal_cards(self, cards: List[int]) -> None:
        if len(cards) not in {3, 17}:
            raise ValueError(
                "Received strange number of cards: should have gotten 17 or 3"
            )
        else:
            self.cards += cards

    def flip_card(self, index_to_flip: int | None = None) -> None:
        if index_to_flip is None:
            self.exposed_cards.append(self.cards[random.randint(0, 16)])
        else:
            self.exposed_cards.append(self.cards[index_to_flip])

    def make_landlord(self, cards: List[int]) -> None:
        self.cards += cards
        self.exposed_cards += cards

    def remove_cards(self, cards: List[int]) -> None:
        for c in cards:
            self.cards.remove(c)
            if c in self.exposed_cards:
                self.exposed_cards.remove(c)
            self.spent_cards.append(c)

    def reset(self) -> None:
        self.cards = []
        self.exposed_cards = []
        self.spent_cards = []

    def has_cards(self, h: None | Hand) -> bool:
        if h is None:
            return True
        hand_count = Counter(h.kicker_cards + h.hand_cards)
        card_count = Counter(self.cards)

        for item, count in hand_count.items():
            if card_count[item] < count:
                return False
        return True
