import pytest
from backend.model.game import Game
from backend.model.player import Player
from backend.game_controller import GameController
from backend.agent.agent import (
    predict,
    convert_to_agent_dict,
    extract_best_move,
    separate_hand_from_kicker,
)

game_dict = {
    "game_id": "VGV39",
    "players": [
        {
            "username": "Tom_U1",
            "uid": "Tom_1",
            "cards": [16, 17],
            "exposed_cards": [16, 17],
            "spent_cards": [
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                3,
                3,
                4,
                4,
                5,
                5,
                6,
                6,
                15,
                15,
            ],
            "last_move": [15, 15],
            "robot": True,
        },
        {
            "username": "Dick_U1",
            "uid": "Dick_1",
            "cards": [3, 4, 5, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 12, 13, 14, 15],
            "exposed_cards": [],
            "spent_cards": [],
            "last_move": None,
        },
        {
            "username": "Harry_U1",
            "uid": "Harry_1",
            "cards": [3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15],
            "exposed_cards": [],
            "spent_cards": [],
            "last_move": None,
        },
    ],
    "current_player": 0,
    "rand_seed": None,
    "landlord": 0,
    "bid": 3,
    "blind": [15, 16, 17],
    "deck": [
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
    ],
    "rounds": [
        [
            (
                "Tom_U1",
                {
                    "base": 1,
                    "chain_length": 8,
                    "low": 7,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [7, 8, 9, 10, 11, 12, 13, 14],
                    "kicker_cards": [],
                    "string_repr": "single-8-chain with no discard",
                },
            ),
            ("Dick_U1", None),
            ("Harry_U1", None),
        ],
        [
            (
                "Tom_U1",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 3,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [3, 3],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard",
                },
            ),
            ("Dick_U1", None),
            ("Harry_U1", None),
        ],
        [
            (
                "Tom_U1",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 4,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [4, 4],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard",
                },
            ),
            ("Dick_U1", None),
            ("Harry_U1", None),
        ],
        [
            (
                "Tom_U1",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 5,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [5, 5],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard",
                },
            ),
            ("Dick_U1", None),
            ("Harry_U1", None),
        ],
        [
            (
                "Tom_U1",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 6,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [6, 6],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard",
                },
            ),
            ("Dick_U1", None),
            ("Harry_U1", None),
        ],
        [
            (
                "Tom_U1",
                {
                    "base": 2,
                    "chain_length": 1,
                    "low": 15,
                    "kicker_base": 0,
                    "kicker_len": 0,
                    "hand_cards": [15, 15],
                    "kicker_cards": [],
                    "string_repr": "pair-1-chain with no discard",
                },
            ),
            ("Dick_U1", None),
            ("Harry_U1", None),
        ],
    ],
    "cur_round": [],
    "started": True,
    "scoreboard": {"Tom_U1": 0, "Dick_U1": 0, "Harry_U1": 0},
    "game_count": 1,
    "n_bombs_played": 0,
}


def test_data_conversion():
    rounds = [
        [(u_name, hd) if hd is not None else (u_name, None) for u_name, hd in rd]
        for rd in game_dict["rounds"]
    ]
    game_dict["rounds"] = rounds
    game = Game(**game_dict)
    from dataclasses import asdict

    assert asdict(convert_to_agent_dict(game)) == {
        "bomb_num": 0,
        "card_play_action_seq": [
            [7, 8, 9, 10, 11, 12, 13, 14],
            [],
            [],
            [3, 3],
            [],
            [],
            [4, 4],
            [],
            [],
            [5, 5],
            [],
            [],
            [6, 6],
            [],
            [],
            [17, 17],
            [],
            [],
        ],
        "last_moves": [[17, 17], [], []],
        "legal_actions": [[20], [20, 30], [30]],
        "num_cards_left": [2, 17, 17],
        "other_hand_cards": [
            3,
            3,
            4,
            4,
            5,
            5,
            6,
            6,
            7,
            7,
            7,
            8,
            8,
            8,
            9,
            9,
            9,
            10,
            10,
            10,
            11,
            11,
            11,
            12,
            12,
            12,
            13,
            13,
            13,
            14,
            14,
            14,
            17,
            17,
        ],
        "played_cards": [
            [7, 8, 9, 10, 11, 12, 13, 14, 3, 3, 4, 4, 5, 5, 6, 6, 17, 17],
            [],
            [],
        ],
        "player_hand_cards": [20, 30],
        "player_position": 0,
        "rival_move": [],
        "three_landlord_cards": [],
    }

    assert extract_best_move(predict(game)).move == [
        16,
        17,
    ]


@pytest.mark.asyncio
async def test_game_controller():
    import os

    os.environ["TEST"] = "True"
    gc = GameController("12345")
    gc.initialize_game(
        [
            Player(username="robot1", uid="1", robot=True),
            Player(username="robot2", uid="2", robot=True),
            Player(username="robot3", uid="3", robot=True),
        ],
        "12345",
        0,
        True,
    )
    await gc.start_game()
    print(gc.g.scoreboard)
    return


def test_triple_single():
    assert separate_hand_from_kicker([3, 3, 3, 5]) == ([3, 3, 3], [5])
    assert separate_hand_from_kicker([3, 3, 3, 5, 5]) == ([3, 3, 3], [5, 5])
    assert separate_hand_from_kicker([3, 3, 3]) == ([3, 3, 3], [])
    assert separate_hand_from_kicker([3, 3]) == ([3, 3], [])
    assert separate_hand_from_kicker([3, 3, 3, 3, 5, 6]) == ([3, 3, 3, 3], [5, 6])

    assert separate_hand_from_kicker([3, 3, 3, 3, 5, 5, 6, 6]) == (
        [3, 3, 3, 3],
        [5, 5, 6, 6],
    )
    assert separate_hand_from_kicker([3, 3, 3, 4, 4, 4, 5, 5, 6, 6]) == (
        [3, 3, 3, 4, 4, 4],
        [5, 5, 6, 6],
    )
    assert separate_hand_from_kicker([3, 3, 3, 4, 4, 4, 5, 6]) == (
        [3, 3, 3, 4, 4, 4],
        [5, 6],
    )
    assert separate_hand_from_kicker([3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 7, 8]) == (
        [3, 3, 3, 4, 4, 4, 5, 5, 5],
        [6, 7, 8],
    )


def test_agent_move_gen():
    from backend.agent.utils.move_generator import MovesGener

    mg = MovesGener([3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 15, 16])
    assert [3, 3, 3, 4, 4, 4, 5, 5] not in mg.gen_moves()
