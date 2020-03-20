import sys
import random
from dlgo.agent.base import Agent
from dlgo.scoring import GameResult

__all__ = [
    'DepthPrunedAgent',
]

MAX_SCORE = 999999
MIN_SCORE = -999999

def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw


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

def best_result(game_state, max_depth, eval_fn):
    # If the game is already over, you know who the winner is.
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE
    # You’ve reached your maximum search depth. Use your heuristic to
    # decide how good this sequence is
    if max_depth == 0:
        return eval_fn(game_state)
    best_so_far = MIN_SCORE
    # Loop over all possible moves
    for candidate_move in game_state.legal_moves():
        # See what the board would look like if you play this move
        next_state = game_state.apply_move(candidate_move)
        # Find the opponent’s best result from this position
        opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
        # Whatever your opponent wants, you want the opposite
        our_result = -1 * opponent_best_result
        # See if this is better than the best result you’ve seen so far
        if our_result > best_so_far:
            best_so_far = our_result

    return best_so_far

# tag::depth-prune-agent[]
class DepthPrunedAgent(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        best_moves = []
        best_score = None
        # Loop over all legal moves.
        for possible_move in game_state.legal_moves():
            # Calculate the game state if we select this move.
            next_state = game_state.apply_move(possible_move)
            # Since our opponent plays next, figure out their best
            # possible outcome from there.
            opponent_best_outcome = best_result(next_state, self.max_depth, self.eval_fn)
            # Our outcome is the opposite of our opponent's outcome.
            our_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or our_best_outcome > best_score:
                # This is the best move so far.
                best_moves = [possible_move]
                best_score = our_best_outcome
            elif our_best_outcome == best_score:
                # This is as good as our previous best move.
                best_moves.append(possible_move)
        # For variety, randomly select among all equally good moves.
        return random.choice(best_moves)
# end::depth-prune-agent[]
