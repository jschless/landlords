from backend.model.hand import Hand
import pytest


class TestHand:
    # Tests for analyzing cards
    def test_classify_empty(self):
        base, chain_length, low = Hand.analyze_cards([])
        assert base == 0
        assert chain_length == 0
        assert low == 0

    def test_classify_solo(self):
        base, chain_length, low = Hand.analyze_cards([3])
        assert base == 1
        assert chain_length == 1
        assert low == 3

    def test_classify_solo_chain(self):
        base, chain_length, low = Hand.analyze_cards([3, 4, 5, 6, 7])
        assert base == 1
        assert chain_length == 5
        assert low == 3

    def test_classify_solo_chain_too_short(self):
        with pytest.raises(ValueError):
            Hand.analyze_cards([3, 4, 5, 6])

    def test_classify_solo_chain_non_consec(self):
        with pytest.raises(ValueError):
            Hand.analyze_cards([3, 4, 5, 6, 8, 9])

    def test_classify_double(self):
        base, chain_length, low = Hand.analyze_cards([3, 3])
        assert base == 2
        assert chain_length == 1
        assert low == 3

    def test_classify_double_chain(self):
        base, chain_length, low = Hand.analyze_cards([3, 3, 4, 4, 5, 5])
        assert base == 2
        assert chain_length == 3
        assert low == 3

    def test_classify_double_chain_too_short(self):
        with pytest.raises(ValueError):
            Hand.analyze_cards([3, 3, 4, 4])

    def test_classify_double_chain_non_consec(self):
        with pytest.raises(ValueError):
            Hand.analyze_cards([3, 3, 4, 4, 6, 6])

    def test_classify_triple(self):
        base, chain_length, low = Hand.analyze_cards([3, 3, 3])
        assert base == 3
        assert chain_length == 1
        assert low == 3

    def test_classify_triple_chain(self):
        base, chain_length, low = Hand.analyze_cards([3, 3, 3, 4, 4, 4])
        assert base == 3
        assert chain_length == 2
        assert low == 3

    def test_classify_triple_chain_non_consec(self):
        with pytest.raises(ValueError):
            Hand.analyze_cards([3, 3, 3, 6, 6, 6])

    ### Tests for analyzing kicker
    def test_classify_kicker_empty(self):
        base, length = Hand.analyze_kicker([])
        assert base == 0
        assert length == 0

    def test_classify_kicker_single(self):
        base, length = Hand.analyze_kicker([3])
        assert base == 1
        assert length == 1

    def test_classify_kicker_two_singles(self):
        base, length = Hand.analyze_kicker([3, 4])
        assert base == 1
        assert length == 2

    def test_classify_kicker_double(self):
        base, length = Hand.analyze_kicker([3, 3])
        assert base == 2
        assert length == 1

    def test_classify_kicker_two_doubles(self):
        base, length = Hand.analyze_kicker([3, 3, 4, 4])
        assert base == 2
        assert length == 2

    def test_classify_kicker_no_mixing(self):
        with pytest.raises(ValueError):
            Hand.analyze_kicker([3, 4, 4])

    def test_classify_kicker_no_triples(self):
        with pytest.raises(ValueError):
            Hand.analyze_kicker([4, 4, 4])

    # Tests for validating kicker with hand
    def test_validate_no_kicker(self):
        assert Hand.validate_kicker_with_hand(1, 5, 0, 0) is True

    def test_validate_solo_kicker(self):
        assert Hand.validate_kicker_with_hand(1, 5, 1, 1) is False

    def test_validate_triple_kicker(self):
        assert Hand.validate_kicker_with_hand(3, 1, 1, 1) is True
        assert Hand.validate_kicker_with_hand(3, 1, 2, 1) is True
        assert Hand.validate_kicker_with_hand(3, 1, 0, 0) is True
        assert Hand.validate_kicker_with_hand(3, 1, 2, 2) is False

    def test_validate_triple_chain_kicker(self):
        assert Hand.validate_kicker_with_hand(3, 2, 1, 2) is True
        assert Hand.validate_kicker_with_hand(3, 2, 2, 2) is True
        assert Hand.validate_kicker_with_hand(3, 2, 2, 3) is False
        assert Hand.validate_kicker_with_hand(3, 2, 0, 0) is True

    def test_validate_bomb_kicker(self):
        assert Hand.validate_kicker_with_hand(3, 2, 1, 2) is True
        assert Hand.validate_kicker_with_hand(3, 2, 2, 2) is True
        assert Hand.validate_kicker_with_hand(3, 2, 2, 3) is False
        assert Hand.validate_kicker_with_hand(3, 2, 0, 0) is True

    # Tests for parsing hand
    def test_parse_hand_solo(self):
        assert Hand.parse_hand([3], []) == Hand(
            base=1,
            chain_length=1,
            low=3,
            kicker_base=0,
            kicker_len=0,
            hand_cards=[3],
            kicker_cards=[],
        )

        with pytest.raises(ValueError):
            Hand.parse_hand([3], [5])
        with pytest.raises(ValueError):
            Hand.parse_hand([2], [])
        with pytest.raises(ValueError):
            Hand.parse_hand([18], [])
        with pytest.raises(ValueError):
            Hand.parse_hand([12, 13, 14, 15, 16, 17], [])

    def test_parse_hand_pair(self):
        assert Hand.parse_hand([3, 3], []) == Hand(
            base=2,
            chain_length=1,
            low=3,
            kicker_base=0,
            kicker_len=0,
            hand_cards=[3, 3],
            kicker_cards=[],
        )

        with pytest.raises(ValueError):
            Hand.parse_hand([3, 3], [5])
        with pytest.raises(ValueError):
            Hand.parse_hand([2, 2], [])
        with pytest.raises(ValueError):
            Hand.parse_hand([3, 3, 4, 4], [])

    def test_parse_hand_pair_chain(self):
        assert Hand.parse_hand([3, 3, 4, 4, 5, 5], []) == Hand(
            base=2,
            chain_length=3,
            low=3,
            kicker_base=0,
            kicker_len=0,
            hand_cards=[3, 3, 4, 4, 5, 5],
            kicker_cards=[],
        )

        with pytest.raises(ValueError):
            Hand.parse_hand([3, 3, 4, 4], [])

    def test_parse_hand_triple(self):
        assert Hand.parse_hand([3, 3, 3], []) == Hand(
            base=3,
            chain_length=1,
            low=3,
            kicker_base=0,
            kicker_len=0,
            hand_cards=[3, 3, 3],
            kicker_cards=[],
        )
        assert Hand.parse_hand([3, 3, 3], [4]) == Hand(
            base=3,
            chain_length=1,
            low=3,
            kicker_base=1,
            kicker_len=1,
            hand_cards=[3, 3, 3],
            kicker_cards=[4],
        )
        assert Hand.parse_hand([3, 3, 3], [4, 4]) == Hand(
            base=3,
            chain_length=1,
            low=3,
            kicker_base=2,
            kicker_len=1,
            hand_cards=[3, 3, 3],
            kicker_cards=[4, 4],
        )

        with pytest.raises(ValueError):
            Hand.parse_hand([3, 3, 3], [2])

    def test_parse_hand_triple_chain(self):
        assert Hand.parse_hand([3, 3, 3, 4, 4, 4], []) == Hand(
            base=3,
            chain_length=2,
            low=3,
            kicker_base=0,
            kicker_len=0,
            hand_cards=[3, 3, 3, 4, 4, 4],
            kicker_cards=[],
        )
        assert Hand.parse_hand([3, 3, 3, 4, 4, 4], [5, 6]) == Hand(
            base=3,
            chain_length=2,
            low=3,
            kicker_base=1,
            kicker_len=2,
            hand_cards=[3, 3, 3, 4, 4, 4],
            kicker_cards=[5, 6],
        )
        assert Hand.parse_hand([3, 3, 3, 4, 4, 4], [5, 5, 6, 6]) == Hand(
            base=3,
            chain_length=2,
            low=3,
            kicker_base=2,
            kicker_len=2,
            hand_cards=[3, 3, 3, 4, 4, 4],
            kicker_cards=[5, 5, 6, 6],
        )

    def test_parse_hand_bombs(self):
        assert Hand.parse_hand([3, 3, 3, 3], []) == Hand(
            base=4,
            chain_length=1,
            low=3,
            kicker_base=0,
            kicker_len=0,
            hand_cards=[3, 3, 3, 3],
            kicker_cards=[],
        )
        assert Hand.parse_hand([16, 17], []) == Hand(
            base=5,
            chain_length=1,
            low=16,
            kicker_base=0,
            kicker_len=0,
            hand_cards=[16, 17],
            kicker_cards=[],
        )
        with pytest.raises(ValueError):
            Hand.parse_hand([16, 17], [3])
