from model.hand import Hand
import pytest


@pytest.mark.parametrize(
    "hand, hand_cards, kicker_cards, expected_moves",
    [
        # Test for pairs
        (
            [3, 4, 5, 5, 6, 7, 7, 7, 9, 9, 9, 11, 11, 12, 14, 15, 15],
            [6, 6],
            [],
            [([7, 7], []), ([9, 9], []), ([11, 11], []), ([15, 15], [])],
        ),
        # Test for triples
        (
            [3, 4, 5, 5, 6, 7, 7, 7, 9, 9, 9, 11, 11, 12, 14, 15, 15],
            [8, 8, 8],
            [],
            [([9, 9, 9], [])],
        ),
        # Test for pair chains
        (
            [3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 9, 9, 9, 11, 11, 12, 14, 15, 15],
            [3, 3, 4, 4, 5, 5],
            [],
            [([4, 4, 5, 5, 6, 6], []), ([5, 5, 6, 6, 7, 7], [])],
        ),
        # Test for triple chains
        (
            [3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 11, 11, 12, 14, 15, 15],
            [4, 4, 4, 5, 5, 5],
            [],
            [([7, 7, 7, 8, 8, 8], []), ([8, 8, 8, 9, 9, 9], [])],
        ),
        # Test for triple single discard
        (
            [3, 5, 5, 5, 7, 7, 7, 9, 9, 9],
            [6, 6, 6],
            [4],
            [
                ([7, 7, 7], [3]),
                ([7, 7, 7], [5]),
                ([7, 7, 7], [9]),
                ([9, 9, 9], [3]),
                ([9, 9, 9], [5]),
                ([9, 9, 9], [7]),
            ],
        ),
        # Test for triple pair discard
        (
            [3, 5, 5, 5, 7, 7, 7, 9, 9, 9],
            [6, 6, 6],
            [4, 4],
            [
                ([7, 7, 7], [5, 5]),
                ([7, 7, 7], [9, 9]),
                ([9, 9, 9], [5, 5]),
                ([9, 9, 9], [7, 7]),
            ],
        ),
        # Test for airplane single discard
        (
            [3, 5, 5, 5, 7, 7, 7, 8, 8, 8],
            [6, 6, 6, 7, 7, 7],
            [4, 7],
            [
                ([7, 7, 7, 8, 8, 8], [3, 5]),
            ],
        ),
        # Test for airplane dual pair discard
        (
            [3, 3, 4, 5, 5, 5, 7, 7, 7, 8, 8, 8],
            [6, 6, 6, 7, 7, 7],
            [4, 4, 7, 7],
            [
                ([7, 7, 7, 8, 8, 8], [3, 3, 5, 5]),
            ],
        ),
        # Test for bomb single discard
        (
            [3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 8],
            [6, 6, 6, 6],
            [4, 5],
            [
                ([8, 8, 8, 8], [3, 4]),
                ([8, 8, 8, 8], [3, 5]),
                ([8, 8, 8, 8], [4, 5]),
            ],
        ),
        # Test for bomb dual discard
        (
            [3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 8, 10, 10],
            [6, 6, 6, 6],
            [4, 4, 5, 5],
            [
                ([8, 8, 8, 8], [3, 3, 5, 5]),
                ([8, 8, 8, 8], [3, 3, 10, 10]),
                ([8, 8, 8, 8], [5, 5, 10, 10]),
            ],
        ),
        # Test for always ultimate bomb
        (
            [3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 8, 10, 10, 16, 17],
            [6, 6, 6, 6],
            [4, 4, 5, 5],
            [
                ([8, 8, 8, 8], [3, 3, 5, 5]),
                ([8, 8, 8, 8], [3, 3, 10, 10]),
                ([8, 8, 8, 8], [5, 5, 10, 10]),
                ([16, 17], []),
            ],
        ),
        # Test for no moves
        ([3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 10, 10, 16], [6, 6, 6, 6], [4, 4, 5, 5], []),
    ],
)
def test_possible_hands(hand, hand_cards, kicker_cards, expected_moves):
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == expected_moves
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b))
