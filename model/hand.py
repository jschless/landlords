from typing import List, Tuple, Dict
from collections import Counter

from pydantic import BaseModel, conint
import itertools

"""
doudizhu hand types:
 Chains:
  - >5 singles
  - >3 pairs
  - >2 trios (2 discards)

 Hand has:
  - base type (solo, double, triple, quad)
  - chain (# consecutive)
  - lowest card (wherever it starts)
  - kicker base (none, # singles, # pairs)
  - kicker len (how many attachments?)
"""


class Hand(BaseModel):
    base: conint(ge=0, le=5)
    chain_length: conint(ge=0, le=13)
    low: conint(ge=3, le=17)
    kicker_base: conint(ge=0, le=2)
    kicker_len: conint(ge=0, le=5)
    hand_cards: List[conint(ge=3, le=17)]
    kicker_cards: List[conint(ge=3, le=17)]
    string_repr: str = None

    @classmethod
    def parse_hand(cls, hand_cards: List[int], kicker_cards: List[int]) -> "Hand":
        # takes a list of cards and kicker cards and pdocues a hand
        if len(hand_cards) == 0 and len(kicker_cards) == 0:
            return None  # represents a pass

        base, chain_length, low = cls.analyze_cards(hand_cards)
        kicker_base, kicker_len = cls.analyze_kicker(kicker_cards)

        if not cls.validate_kicker_with_hand(
            base, chain_length, kicker_base, kicker_len
        ):
            raise ValueError("Kicker is incompatible with given hand")

        return cls(
            base=base,
            chain_length=chain_length,
            low=low,
            kicker_base=kicker_base,
            kicker_len=kicker_len,
            hand_cards=hand_cards,
            kicker_cards=kicker_cards,
        )

    def serialize(self):
        self.string_repr = self.__str__()
        return self.model_dump(mode="json")

    @staticmethod
    def longest_consecutive_chain(nums: List[int]) -> int:
        # Returns the largest consecutive chain in the list of ints
        nums = sorted(set(nums))
        longest = current = 1 if nums else 0

        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] + 1:
                current += 1
            else:
                longest = max(longest, current)
                current = 1

        return max(longest, current)

    @classmethod
    def analyze_cards(cls, cards: List[int]) -> Tuple[int, int, int]:
        # analyzes cards to produce a hand
        if len(cards) == 2 and sorted(cards) == [16, 17]:
            # bomb
            return 5, 1, 16
        if len(cards) == 0:
            return 0, 0, 0
        counts = Counter(cards)
        if len(set(counts.values())) != 1:
            raise ValueError(f"Invalid hand type: inconsistent hand base {cards}")
        base = next(iter(counts.values()))
        chain_length = cls.longest_consecutive_chain(list(counts.keys()))

        cls.validate_hand_type(base, chain_length, cards)

        return base, chain_length, min(cards)

    @staticmethod
    def validate_hand_type(base: int, chain_length: int, cards: int) -> None:
        # Final checks on hand type
        if base == 1 and chain_length < 5 and chain_length > 1:
            raise ValueError(f"Invalid hand type: solo with chain < 5 {cards}")
        if chain_length > 1 and (16 in cards or 17 in cards):
            raise ValueError(f"Invalid hand type: jokers can't be in chain {cards}")
        if base == 2 and chain_length < 3 and chain_length > 1:
            raise ValueError(f"Invalid hand type: double with chain < 3 {cards}")

        if base * chain_length != len(cards):
            raise ValueError(f"Invalid hand type: base*chain_length != n_cards {cards}")

    @classmethod
    def analyze_kicker(cls, cards: List[int]) -> Tuple[int, int]:
        # returns base type and n_cards for kicker.
        if len(cards) == 0:
            return 0, 0
        counts = Counter(cards)
        if len(set(counts.values())) != 1:
            raise ValueError(f"Invalid kicker type: inconsistent hand base {cards}")
        base = next(iter(counts.values()))
        if base > 2:
            raise ValueError(f"Invalid kicker type: must be less than 2 {cards}")

        return base, len(counts)

    @staticmethod
    def validate_kicker_with_hand(
        base: int, chain_length: int, kicker_base: int, kicker_len: int
    ) -> bool:
        # Return whether kicker is valid with given hand
        # DISCARDS:
        # - Triple: you get equal to chain length
        # - Quad: You get two
        if kicker_base == 0 and kicker_len == 0:
            # it's always valid to have no kicker
            return True
        elif base == 3:
            return kicker_len == chain_length
        elif base == 4:
            return kicker_len == 2
        elif base == 5:
            return kicker_len == 0
        return False

    def is_valid_successor(self, succ: "Hand") -> bool:
        """Returns true if the proposed next hand is valid

        A few things must hold:
        - must be of same base and length
        - low must be higher
        - kicker base and length must match

        OR we need a bomb
        """
        if succ.is_bomb() or succ is None:
            return True
        elif (
            self.base == succ.base
            and self.chain_length == succ.chain_length
            and self.kicker_base == succ.kicker_base
            and self.kicker_len == succ.kicker_len
            and self.low < succ.low
        ):
            return True
        else:
            return False

    def is_bomb(self) -> bool:
        # Returns true if this hand is a bomb
        if self.base == 4 and self.kicker_base == 0 or self.base == 5:
            return True

    def __str__(self):
        return self.label_hand() + " with " + self.label_discard()

    def label_hand(self) -> str:
        """Returns a string representation of the hand"""
        if self.base == 0:
            return "empty"
        elif self.base == 1 and self.chain_length == 0:
            return "single"
        elif self.base == 1 and self.chain_length > 0:
            return f"single-{self.chain_length}-chain"
        elif self.base == 2 and self.chain_length == 0:
            return "pair"
        elif self.base == 2 and self.chain_length > 0:
            return f"pair-{self.chain_length}-chain"
        elif self.base == 3 and self.chain_length == 0:
            return "triple"
        elif self.base == 3 and self.chain_length > 0:
            return f"triple-{self.chain_length}-chain"
        elif self.base == 4:
            return f"bomb"
        elif self.base == 5:
            return f"ultimate bomb"

        raise ValueError("Should not be reachable")

    def label_discard(self) -> str:
        if self.kicker_base == 0:
            return "no discard"
        elif self.kicker_base == 1:
            return f"{self.kicker_len} single discards"
        elif self.kicker_base == 2:
            return f"{self.kicker_len} pair discards"

        raise ValueError("Should not be reachable")

    def possible_hands(self, cards: List[int]) -> List["Hand"]:
        # Generates the possible hands that can work for a given hand set

        c = Counter(cards)

        # prune things less than base
        card_freqs = {}
        for num, freq in c.items():
            if freq >= self.base and num > self.low:
                card_freqs[num] = freq

        print(card_freqs)
        # try to build chains starting from each combo
        final_hands = []

        for num, freq in card_freqs.items():
            temp = can_build_chain(card_freqs, num, self.chain_length, self.base)
            if temp is not None:
                final_hands.append(temp)

        possible_combos = []
        print(f"Final hands: {final_hands}")
        if self.kicker_len != 0:
            for h in final_hands:
                final_kickers = self.room_for_kicker(
                    cards, h, self.kicker_base, self.kicker_len
                )
                print(f"kicker options are {final_kickers}")

                possible_combos += [(h, kick) for kick in final_kickers]
        else:
            possible_combos = [(h, []) for h in final_hands]

        if 16 in cards and 17 in cards:
            possible_combos.append(([16, 17], []))

        return possible_combos

    def room_for_kicker(self, cards, test_hand, kicker_base, kicker_size):
        # remove
        if kicker_base == 0:
            return []
        temp_cards = cards[:]
        for c in test_hand:
            temp_cards.remove(c)

        c = {
            num: freq
            for num, freq in Counter(temp_cards).items()
            if freq >= kicker_base
        }
        if len(c) >= kicker_size:
            # get all permutations
            kicker_options = []
            for combo in itertools.combinations(c.keys(), kicker_size):
                kicker_options.append(sorted(list(combo) * kicker_base))
            return kicker_options

        return []


def can_build_chain(freqs: Dict[int, int], start: int, length: int, freq: int) -> bool:
    # Returns the largest consecutive chain in the list of ints
    chain = [start] * freq
    for i in range(1, length):
        if start + i not in freqs:
            return None
        else:
            chain += [start + i] * freq
    return chain
