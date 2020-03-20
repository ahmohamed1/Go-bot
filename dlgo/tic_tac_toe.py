import random


def find_winning_move(game_state, next_player):
    # Loops over all legal moves
    for candidate_move in game_state.legal_move(next_player):
        #Calculates what the board would look like if you pick this move
        next_state = game_state.apply_move(candidate_move)
        # This is a winning move! No need to continue searching.
        if next_state.is_over() and next_state.winner == next_player:
            return candidate_move
    # Can’t win on this turn
    return None

def eliminate_losing_moves(game_state, next_player):
    opponent = next_player.other()
    # possible_moves will become a list of all moves worth considering
    possible_move = []
    for candidate_move in game_state.legal_move(next_player):
        # Calculates what the board would look like if you play this move
        next_state = game_state.apply_move(candidate_move)
        # Does this give your opponent a winning move? If not, this move is plausible
        opponent_winning_move = find_winning_move(next_state, opponent)
        if opponent_winning_move is None:
            possible_move.append(candidate_move)
    return possible_move

def find_two_step_win(game_state, next_player):
    opponent = next_player.other()
    # Loops over all legal moves
    for candidate_move in game_state.legal_move(next_player):
        # Calculates what the board would look like if you play this move
        next_state = game_state.apply_move(candidate_move)
        # Does your opponent have a good defense? If not, pick this move.
        good_responses = eliminate_losing_moves(game_state, opponent)
        if not good_responses:
            return candidate_move
    # No matter what move you pick, your opponent can prevent a win
    return None
