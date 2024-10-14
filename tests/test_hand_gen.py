from model.hand import Hand
import pytest


def test_pairs():
    hand = [3, 4, 5, 5, 6, 7, 7, 7, 9, 9, 9, 11, 11, 12, 14, 15, 15]
    hand_cards = [6, 6]
    kicker_cards = []
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([7, 7], []),
        ([9, 9], []),
        ([11, 11], []),
        ([15, 15], []),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_triples():
    hand = [3, 4, 5, 5, 6, 7, 7, 7, 9, 9, 9, 11, 11, 12, 14, 15, 15]
    hand_cards = [8, 8, 8]
    kicker_cards = []
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([9, 9, 9], []),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_pair_chains():
    hand = [3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 9, 9, 9, 11, 11, 12, 14, 15, 15]
    hand_cards = [3, 3, 4, 4, 5, 5]
    kicker_cards = []
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([4, 4, 5, 5, 6, 6], []),
        ([5, 5, 6, 6, 7, 7], []),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_triple_chains():
    hand = [3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 11, 11, 12, 14, 15, 15]
    hand_cards = [4, 4, 4, 5, 5, 5]
    kicker_cards = []
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([7, 7, 7, 8, 8, 8], []),
        ([8, 8, 8, 9, 9, 9], []),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_triple_single_discard():
    hand = [3, 5, 5, 5, 7, 7, 7, 9, 9, 9]
    hand_cards = [6, 6, 6]
    kicker_cards = [4]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([7, 7, 7], [3]),
        ([7, 7, 7], [5]),
        ([7, 7, 7], [9]),
        ([9, 9, 9], [3]),
        ([9, 9, 9], [5]),
        ([9, 9, 9], [7]),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_triple_pair_discard():
    hand = [3, 5, 5, 5, 7, 7, 7, 9, 9, 9]
    hand_cards = [6, 6, 6]
    kicker_cards = [4, 4]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([7, 7, 7], [5, 5]),
        ([7, 7, 7], [9, 9]),
        ([9, 9, 9], [5, 5]),
        ([9, 9, 9], [7, 7]),
    ]

    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_airplane_single_discard():
    hand = [3, 5, 5, 5, 7, 7, 7, 8, 8, 8]
    hand_cards = [6, 6, 6, 7, 7, 7]
    kicker_cards = [
        4,
        7,
    ]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([7, 7, 7, 8, 8, 8], [3, 5]),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_airplane_dual_pair_discard():
    hand = [3, 3, 4, 5, 5, 5, 7, 7, 7, 8, 8, 8]
    hand_cards = [6, 6, 6, 7, 7, 7]
    kicker_cards = [
        4,
        4,
        7,
        7,
    ]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([7, 7, 7, 8, 8, 8], [3, 3, 5, 5]),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_bomb_single_discard():
    hand = [3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 8]
    hand_cards = [6, 6, 6, 6]
    kicker_cards = [4, 5]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([8, 8, 8, 8], [3, 4]),
        ([8, 8, 8, 8], [3, 5]),
        ([8, 8, 8, 8], [4, 5]),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_bomb_dual_discard():
    hand = [3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 8, 10, 10]
    hand_cards = [6, 6, 6, 6]
    kicker_cards = [4, 4, 5, 5]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == [
        ([8, 8, 8, 8], [3, 3, 5, 5]),
        ([8, 8, 8, 8], [3, 3, 10, 10]),
        ([8, 8, 8, 8], [5, 5, 10, 10]),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_always_ultimate_bomb():
    hand = [3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 8, 10, 10, 16, 17]
    hand_cards = [6, 6, 6, 6]
    kicker_cards = [4, 4, 5, 5]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)

    assert moves == [
        ([8, 8, 8, 8], [3, 3, 5, 5]),
        ([8, 8, 8, 8], [3, 3, 10, 10]),
        ([8, 8, 8, 8], [5, 5, 10, 10]),
        ([16, 17], []),
    ]
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True


def test_no_moves():
    hand = [3, 3, 4, 5, 5, 5, 5, 8, 8, 8, 10, 10, 16]
    hand_cards = [6, 6, 6, 6]
    kicker_cards = [4, 4, 5, 5]
    h = Hand.parse_hand(hand_cards, kicker_cards)
    moves = h.possible_hands(hand)
    assert moves == []
    for a, b in moves:
        assert h.is_valid_successor(Hand.parse_hand(a, b)) == True
