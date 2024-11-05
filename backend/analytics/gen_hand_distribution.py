import random
from agent.utils.move_generator import MovesGener


def gen_random_hand():
    deck = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    deck *= 4
    deck.extend([20, 30])
    random.shuffle(deck)
    return deck[:17]


def get_stats(stat_func, N: int = 1_000):
    return [stat_func(gen_random_hand()) for _ in range(N)]


def gen_possible_move_length(hand):
    """
    here are the quartiles for 10_000 randomly generated hands

    0.0 ----> 17.0
    0.1 ----> 23.0
    0.2 ----> 32.0
    0.3 ----> 33.0
    0.4 ----> 36.0
    0.5 ----> 41.0
    0.6 ----> 44.0
    0.7 ----> 47.0
    0.8 ----> 57.0
    0.9 ----> 78.0
    1.0 ----> 158.0
    """
    mg = MovesGener(hand)
    return len(mg.gen_moves())


def gen_weighted_possible_move_lengths():
    # TODO
    pass


def make_bet_by_move_length(hand_cards: int):
    move_length = gen_possible_move_length(hand_cards)
    if move_length < 36:
        return 0
    elif move_length < 44:
        return 1
    elif move_length < 60:
        return 2
    else:
        return 3
