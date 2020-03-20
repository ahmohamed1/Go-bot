from dlgo import gotypes

def capture_diff(game_state):
    black_stones = 0
    white_stones = 0
    for r in range(1, game_state.board.num_rows +1):
        for c in range(1, game_state.board.num_cols +1):
            p = gotypes.Point(r, c)
            color = game_state.board.get(p)
            if color == gotypes.Player.black:
                black_stones += 1
            elif color == gotypes.Player.white:
                white_stones += 1
    # Calculate the difference between the number of black stones and white
    # stones on the board. This will be the same as the difference in the
    # number of captures, unless one player passes early
    diff = black_stones - white_stones
    # If it’s black’s move, return (black stones) – (white stones)
    if game_state.next_player == gotypes.Player.black:
        return diff
    # If it’s white’s move, return (white stones) – (black stones)
    return -1 * diff
