import pytest
from .utils import format_move, execute_moves_multiple
from .conftest import complete_game_p1_blowout, complete_game_p3_blowout


@pytest.mark.asyncio
async def test_concurrent_complete_rounds(fastapi_server):
    game1 = complete_game_p3_blowout()
    game2 = complete_game_p1_blowout()
    results = await execute_moves_multiple(fastapi_server, [game1, game2])
    tom, dick, harry = tuple(results[:3])

    assert len(harry["my_cards"]) == 0
    assert len(tom["my_cards"]) == 17
    assert dick["scoreboard"][harry["username"]] == 12
    assert tom["scoreboard"][dick["username"]] == -6

    tom, dick, harry = tuple(results[3:])
    assert len(harry["my_cards"]) == 17
    assert len(tom["my_cards"]) == 0
    assert dick["scoreboard"][tom["username"]] == 12
    assert tom["scoreboard"][dick["username"]] == -6
