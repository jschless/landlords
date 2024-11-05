from agent.utils.move_generator import MovesGener


def test_gen_moves():
    mg = MovesGener([3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 15, 20, 30])
    check = [3, 3, 3, 3, 5, 5] not in mg.gen_type_13_4_2()
    assert check
