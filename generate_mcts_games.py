import argparse
import numpy as np

from dlgo.encoders.base import get_encoder_by_name
from dlgo import goboard_fast as goboard
from dlgo.agent.mcts import mcts
from dlgo.utils import print_board, print_move

def generate_game(board_size, rounds, max_moves, temperature):
    # In boards you store encoded board state; moves is for encoded moves
    boards, moves = [] , []

    # Initialize a OnePlaneEncoder by name with given board size
    encoder = get_encoder_by_name('oneplane', board_size)

    # A new game of size board_size is instantiated
    game = goboard.GameState.new_game(board_size)

    # A Monte Carlo treesearch agent with specified number of rounds and
    # temperature will serve as your bot
    bot = mcts.MCTSAgent(rounds, temperature)

    num_moves = 0

    while not game.is_over():
        print_board(game.board)
        # The next move is selected by the bot
        move = bot.select_move(game)
        if move.is_play:
            # The encoded board situation is appended to boards
            boards.append(encoder.encode(game))
            # The onehotencoded next move is appended to moves
            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot)

        print_move(game.next_player, move)
        # Afterward, the bot move is applied to the board
        game = game.apply_move(move)
        num_moves += 1
        # You continue with the next move, unless the maximum number of moves has been reached
        if num_moves > max_moves:
            break

    return np.array(boards), np.array(moves)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size','-b',type=int, default=9)
    parser.add_argument('--rounds','-r',type=int, default=1000)
    parser.add_argument('--temperature','-t',type=float, default=1.8)
    parser.add_argument('--max_moves','-m',type=int, default=60,
                        help='Max moves per game.')
    parser.add_argument('--num_games','-n',type=int, default=10)
    parser.add_argument('--board_out', default = 'features.npy')
    parser.add_argument('--move_out', default = 'labels.npy')

    args = parser.parse_args()
    xs = []
    ys = []
    for i in range(args.num_games):
        print('Generating game %d/%d...' % (i + 1, args.num_games))
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)
        x = np.concatenate(xs)
        y = np.concatenate(ys)
        np.save(args.board_out, x)
        np.save(args.move_out, y)

if __name__ == '__main__':
    main()
