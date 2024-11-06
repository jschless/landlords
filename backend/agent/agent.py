import itertools

from collections import namedtuple
from model.game import Game
from agent.utils.move_generator import MovesGener
from agent.utils import move_detector as md, move_selector as ms, utils
from agent.deep import DeepAgent
from dataclasses import dataclass, field


PossibleMove = namedtuple("Move", ["move", "move_type", "win_rate", "result"])


def convert_list_to_agent(xs: list[int]) -> list[int]:
    """Maps cards from game space to agent space"""
    card_to_agent_card = {15: 17, 16: 20, 17: 30}
    return [card_to_agent_card.get(x, x) for x in xs]


def convert_to_agent_dict(game: Game) -> dict:
    player = game.players[game.current_player]
    # 0 is landlord, 1 is first peasant, 2 is second peasant

    player_position = (game.landlord - game.current_player) % 3
    iter_order = [(game.landlord + i) % 3 for i in range(3)]

    player_hand_cards = convert_list_to_agent(player.cards)
    num_cards_left = [len(game.players[i].cards) for i in iter_order]

    three_landlord_cards = convert_list_to_agent(
        game.players[game.landlord].landlord_cards
    )

    card_play_action_seq = []
    for rd in [*game.rounds, game.cur_round]:
        for _, hd in rd:
            if hd is None or hd == []:
                card_play_action_seq.append([])
            else:
                hd_cards = hd["hand_cards"] + hd["kicker_cards"]
                card_play_action_seq.append(convert_list_to_agent(hd_cards))

    other_hand_cards = []
    for p in game.players:
        if p is not player:
            other_hand_cards.extend(convert_list_to_agent(p.cards))
    other_hand_cards.sort()

    last_moves = []
    for i in iter_order:
        last_move = []
        if game.players[i].last_move:
            last_move = game.players[i].last_move

        last_moves.append(convert_list_to_agent(last_move))

    # Played cards
    played_cards = [
        convert_list_to_agent(game.players[i].spent_cards) for i in iter_order
    ]

    bomb_num = game.n_bombs_played

    # Get rival move and legal_actions
    rival_move = []
    if len(card_play_action_seq) != 0:
        if len(card_play_action_seq[-1]) == 0:
            rival_move = card_play_action_seq[-2]
        else:
            rival_move = card_play_action_seq[-1]

    info_set = InfoSet(
        player_position=player_position,
        player_hand_cards=player_hand_cards,
        num_cards_left=num_cards_left,
        three_landlord_cards=three_landlord_cards,
        card_play_action_seq=card_play_action_seq,
        other_hand_cards=other_hand_cards,
        last_moves=last_moves,
        played_cards=played_cards,
        bomb_num=bomb_num,
        rival_move=rival_move,
        legal_actions=_get_legal_card_play_actions(player_hand_cards, rival_move),
    )

    return info_set


def predict(game: Game, agent: DeepAgent) -> list[PossibleMove]:
    """Takes a game and then an agent and returns a list of three or fewer moves"""
    info_set = convert_to_agent_dict(game)

    actions, actions_confidence = agent.act(info_set)
    moves = []

    agent_card_to_card = {17: 15, 20: 16, 30: 17}
    actions = [[agent_card_to_card.get(a, a) for a in action] for action in actions]
    move_types = [md.get_move_type(action) for action in actions]

    for i in range(len(actions)):
        # Here, we calculate the win rate
        win_rate = max(actions_confidence[i], -1)
        win_rate = min(win_rate, 1)
        moves.append(
            PossibleMove(
                move=actions[i],
                move_type=move_types[i],
                win_rate=str(round((win_rate + 1) / 2, 4)),
                result=str(round(actions_confidence[i], 6)),
            )
        )

    return moves


def separate_hand_from_kicker(cards: list[int]) -> tuple[list[int], list[int]]:
    # Given a prediction (list of cards), determine what is the hand and kicker and return
    mt = md.get_move_type(cards)

    discard_types = set(
        [
            utils.TYPE_6_3_1,
            utils.TYPE_7_3_2,
            utils.TYPE_13_4_2,
            utils.TYPE_14_4_22,
            utils.TYPE_11_SERIAL_3_1,
            utils.TYPE_12_SERIAL_3_2,
        ]
    )
    if mt["type"] in discard_types:
        hand_cards, kicker_cards = [], []
        for c in cards:
            if c >= mt["rank"] and c < mt["rank"] + mt.get("len", 1):
                hand_cards.append(c)
            else:
                kicker_cards.append(c)
        return hand_cards, kicker_cards
    else:
        return cards, []


def extract_best_move(moves: list[PossibleMove]) -> PossibleMove:
    return max(moves, key=lambda x: x.win_rate)


@dataclass
class InfoSet:
    player_position: int | None = None
    player_hand_cards: list[int] = field(default_factory=list)
    num_cards_left: int = 0
    three_landlord_cards: list[int] = field(default_factory=list)
    card_play_action_seq: list[int] = field(default_factory=list)
    other_hand_cards: list[int] = field(default_factory=list)
    last_moves: list[int] = field(default_factory=list)
    played_cards: list[int] = field(default_factory=list)
    bomb_num: int = 0
    rival_move: int | None = None
    legal_actions: list[int] = field(default_factory=list)


def _get_legal_card_play_actions(
    player_hand_cards: list[int], rival_move: list[int]
) -> list[list[int]]:
    mg = MovesGener(player_hand_cards)

    rival_type = md.get_move_type(rival_move)
    rival_move_type = rival_type["type"]
    rival_move_len = rival_type.get("len", 1)
    moves = list()

    if rival_move_type == utils.TYPE_0_PASS:
        moves = mg.gen_moves()

    elif rival_move_type == utils.TYPE_1_SINGLE:
        all_moves = mg.gen_type_1_single()
        moves = ms.filter_type_1_single(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_2_PAIR:
        all_moves = mg.gen_type_2_pair()
        moves = ms.filter_type_2_pair(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_3_TRIPLE:
        all_moves = mg.gen_type_3_triple()
        moves = ms.filter_type_3_triple(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_4_BOMB:
        all_moves = mg.gen_type_4_bomb() + mg.gen_type_5_king_bomb()
        moves = ms.filter_type_4_bomb(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_5_KING_BOMB:
        moves = []

    elif rival_move_type == utils.TYPE_6_3_1:
        all_moves = mg.gen_type_6_3_1()
        moves = ms.filter_type_6_3_1(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_7_3_2:
        all_moves = mg.gen_type_7_3_2()
        moves = ms.filter_type_7_3_2(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_8_SERIAL_SINGLE:
        all_moves = mg.gen_type_8_serial_single(repeat_num=rival_move_len)
        moves = ms.filter_type_8_serial_single(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_9_SERIAL_PAIR:
        all_moves = mg.gen_type_9_serial_pair(repeat_num=rival_move_len)
        moves = ms.filter_type_9_serial_pair(all_moves, rival_move)
    elif rival_move_type == utils.TYPE_10_SERIAL_TRIPLE:
        all_moves = mg.gen_type_10_serial_triple(repeat_num=rival_move_len)
        moves = ms.filter_type_10_serial_triple(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_11_SERIAL_3_1:
        all_moves = mg.gen_type_11_serial_3_1(repeat_num=rival_move_len)
        moves = ms.filter_type_11_serial_3_1(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_12_SERIAL_3_2:
        all_moves = mg.gen_type_12_serial_3_2(repeat_num=rival_move_len)
        moves = ms.filter_type_12_serial_3_2(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_13_4_2:
        all_moves = mg.gen_type_13_4_2()
        moves = ms.filter_type_13_4_2(all_moves, rival_move)

    elif rival_move_type == utils.TYPE_14_4_22:
        all_moves = mg.gen_type_14_4_22()
        moves = ms.filter_type_14_4_22(all_moves, rival_move)

    if rival_move_type not in [
        utils.TYPE_0_PASS,
        utils.TYPE_4_BOMB,
        utils.TYPE_5_KING_BOMB,
    ]:
        moves = moves + mg.gen_type_4_bomb() + mg.gen_type_5_king_bomb()

    if len(rival_move) != 0:  # rival_move is not 'pass'
        moves = moves + [[]]

    for m in moves:
        m.sort()

    moves.sort()
    moves = list(move for move, _ in itertools.groupby(moves))

    return moves
