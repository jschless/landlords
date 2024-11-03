from backend.model.player import Player
import pytest


class TestPlayer:
    def test_make_player(self):
        user = Player(username="joe", uid="random_12345")
        assert len(user.cards) == 0
        user.deal_cards([3] * 17)
        user.deal_cards([3] * 3)
        with pytest.raises(ValueError):
            user.deal_cards([3] * 20)
