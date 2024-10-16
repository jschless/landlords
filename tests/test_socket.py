import pytest
from .utils import format_move, execute_moves_multiple


@pytest.mark.asyncio
async def test_through_bet(fastapi_server):
    p1 = [{"action": "bet", "bet": "1"}]
    p2 = [{"action": "bet", "bet": "2"}]
    p3 = [{"action": "bet", "bet": "3"}]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])
    tom, dick, harry = tuple(results)

    assert harry["landlord"] == 2
    assert len(harry["my_cards"]) == 20


@pytest.mark.asyncio
async def test_through_first_move(fastapi_server):
    p1 = [{"action": "bet", "bet": "3"}, format_move([3, 3], [])]
    p2 = [format_move([7, 7], [])]
    p3 = [format_move([11, 11], [])]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    tom, dick, harry = tuple(results)

    assert tom["my_cards"].count(3) == 0
    assert len(tom["my_cards"]) == 18
    for p in tom["players"]:
        if p["username"] == harry["username"]:
            # Landlord has played two cards (20 - 18)
            assert p["n_cards"] == 15
        else:
            assert p["n_cards"] == 15


@pytest.mark.asyncio
async def test_complete_hand(fastapi_server):
    """
    P3 wins the round of betting.
    P3 opens with a 6 card straight.
    P1 wins with a better hand.
    Everyone passes until P1 wins
    """
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([6, 7, 8, 9, 10, 11], []),
    ]
    p2 = [{"action": "bet", "bet": "2"}, format_move([], [])]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8], []),
        format_move([], []),
    ]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    tom, dick, harry = tuple(results)
    assert len(tom["my_cards"]) == 11
    assert tom["current_player"] == 0


@pytest.mark.asyncio
async def test_complete_round(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([], []),
        format_move([], []),
    ]
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], []),
        format_move([11, 12, 13, 14, 15], []),
        format_move([16, 17], []),
    ]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    tom, dick, harry = tuple(results)

    assert len(harry["my_cards"]) == 0
    assert len(tom["my_cards"]) == 17

    assert harry["scoreboard"][harry["username"]] == 12


@pytest.mark.asyncio
async def test_two_rounds(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([], []),
        format_move([], []),
    ] * 2
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ] * 2
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], []),
        format_move([11, 12, 13, 14, 15], []),
        format_move([16, 17], []),
        {"action": "play_again", "decision": True},
    ] * 2

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])
    tom, dick, harry = tuple(results)
    assert harry["scoreboard"][harry["username"]] == 24


@pytest.mark.asyncio
async def test_invalid_start_move(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([6, 7, 8, 9, 10], []),
    ]
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 5, 6, 7, 8], []),  # bad move
        format_move([3, 4, 5, 6, 7], []),  # correct move
        format_move([], []),
    ]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    # So Tom should be current_play
    tom, dick, harry = tuple(results)

    assert tom["current_player"] == 0

    assert len(harry["my_cards"]) == 15
    assert len(tom["my_cards"]) == 12
    assert len(dick["my_cards"]) == 17


@pytest.mark.asyncio
async def test_invalid_following_move(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([6, 7, 8, 9, 10, 11], []),
        format_move([], []),
    ]
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
    ]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 5, 6, 7, 8], []),  # bad move
        format_move([3, 4, 5, 6, 7], []),  # correct move
    ]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    tom, dick, harry = tuple(results)
    assert tom["current_player"] == 2

    assert len(harry["my_cards"]) == 15
    assert len(tom["my_cards"]) == 17
    assert len(dick["my_cards"]) == 17


@pytest.mark.asyncio
async def test_invalid_following_move_2(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "3"},
        format_move([6, 7, 8, 9, 10, 11], []),
    ]
    p2 = [
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        format_move([3, 4, 5, 6, 7, 8], []),  # bad move because its smaller
        format_move([], []),
    ]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    tom, dick, harry = tuple(results)
    assert tom["current_player"] == 0

    assert len(harry["my_cards"]) == 17
    assert len(tom["my_cards"]) == 14
    assert len(dick["my_cards"]) == 17


@pytest.mark.asyncio
async def test_skip_on_three_bad_submissions(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "3"},
        format_move([6, 7, 8, 9, 10], []),
    ]
    p2 = [
        format_move([], []),
    ]
    p3 = [
        format_move([3, 5, 6, 7, 8], []),  # bad move
        format_move([3, 5, 6, 7, 8], []),  # bad move
        format_move([3, 5, 6, 7, 8], []),  # bad move
        format_move([3, 4, 5, 6, 7], []),  # correct move, but shoudln't happen
        format_move([], []),
    ]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    tom, dick, harry = tuple(results)
    assert tom["current_player"] == 0

    assert len(harry["my_cards"]) == 17
    assert len(tom["my_cards"]) == 15
    assert len(dick["my_cards"]) == 17


@pytest.mark.asyncio
async def test_submitting_fake_cards(fastapi_server):
    p1 = [
        {"action": "bet", "bet": "1"},
        format_move([], []),
        format_move([10], []),
    ]
    p2 = [
        {"action": "bet", "bet": "2"},
        format_move([], []),
        format_move([], []),
    ]
    p3 = [
        {"action": "bet", "bet": "3"},
        format_move([3, 4, 5, 6, 7, 8], []),
        format_move([3, 4, 5, 6, 7, 8], []),  # Doesn't have these cards anymore
        format_move([9], []),
    ]

    results = await execute_moves_multiple(fastapi_server, [(p1, p2, p3)])

    tom, dick, harry = tuple(results)

    assert len(harry["my_cards"]) == 13
    assert len(tom["my_cards"]) == 16
    assert len(dick["my_cards"]) == 17


@pytest.mark.asyncio
async def test_submitting_bad_kicker():
    # TODO: add a new test deal that has more exciting card combos
    pass


@pytest.mark.asyncio
async def test_start_round_with_pass():
    # TODO: add a new test deal that has more exciting card combos
    assert True == False


@pytest.mark.asyncio
async def test_submit_bad_hands_3_times():
    # TODO: add a new test deal that has more exciting card combos
    assert True == False
