import pytest
from .utils import execute_moves_multiple


@pytest.mark.asyncio
async def test_disconnect_at_start(fastapi_server, complete_game_p3_blowout):
    ###
    pass


@pytest.mark.parametrize("player_to_test", [0, 1, 2])
@pytest.mark.parametrize("disconnect_round", [1, 2, 3])
@pytest.mark.asyncio
async def test_disconnect(
    fastapi_server, complete_game_p3_blowout, player_to_test, disconnect_round
):
    # Some are failing bc: when they disconnect, the server keeps sending stuff, and then you get
    # bombarded with move requests...
    p1, p2, p3 = complete_game_p3_blowout

    results = await execute_moves_multiple(
        fastapi_server, [(p1, p2, p3)], player_to_test, disconnect_round
    )
    tom, dick, harry = tuple(results)

    assert len(tom["my_cards"]) == 17
    assert len(harry["my_cards"]) == 0
    assert dick["scoreboard"][harry["username"]] == 12
    assert tom["scoreboard"][dick["username"]] == -6


@pytest.mark.parametrize("player_to_test", [0, 1, 2])
@pytest.mark.parametrize("disconnect_round", [1, 2, 3, 4, 5, 6])
@pytest.mark.asyncio
async def test_disconnect_consecutive_games(
    fastapi_server, complete_game_p3_blowout, player_to_test, disconnect_round
):
    p1, p2, p3 = complete_game_p3_blowout
    p1 *= 2
    p2 *= 2
    p3.append({"action": "play_again", "decision": True})
    p3 *= 2
    p3.pop()

    results = await execute_moves_multiple(
        fastapi_server, [(p1, p2, p3)], player_to_test, disconnect_round
    )
    tom, dick, harry = tuple(results)

    assert len(tom["my_cards"]) == 17
    assert len(harry["my_cards"]) == 0
    assert dick["scoreboard"][harry["username"]] == 24
    assert tom["scoreboard"][dick["username"]] == -12
