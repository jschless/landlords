from model.game import Game
from model.player import Player
import pytest


class TestGame:
    def test_gen_game_data(self, midprocess_game):
        assert midprocess_game.game_data("Harry") == {
            "game_id": "569IR",
            "username": "Harry_U",
            "my_cards": [
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                11,
                12,
                12,
                13,
                13,
                14,
                14,
                15,
                15,
                16,
                17,
            ],
            "players": [
                {"username": "Tom_U", "n_cards": 17, "exposed_cards": [3]},
                {"username": "Dick_U", "n_cards": 17, "exposed_cards": []},
            ],
            "landlord": 2,
            "started": True,
            "action": "update",
        }


@pytest.fixture(scope="module")
def midprocess_game():
    p1 = Player(
        username="Tom_U",
        uid="Tom",
        cards=[3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        exposed_cards=[3],
        spent_cards=[],
    )
    p2 = Player(
        username="Dick_U",
        uid="Dick",
        cards=[3, 4, 5, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 12, 13, 14, 15],
        exposed_cards=[],
        spent_cards=[],
    )
    p3 = Player(
        username="Harry_U",
        uid="Harry",
        cards=[3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 17],
        exposed_cards=[15, 16, 17],
        spent_cards=[],
    )

    game = Game(
        game_id="569IR",
        players=[p1, p2, p3],
        current_player=0,
        rand_seed=None,
        landlord=2,
        blind=[15, 16, 17],
        deck=[
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
        rounds=[],
        started=True,
    )
    return game
