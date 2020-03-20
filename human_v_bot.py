from dlgo.agent import naive
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_move, print_board, point_from_coords
from six.moves import input

from dlgo import evaluate_functions
from dlgo.agent import depthpruning

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = depthpruning.DepthPrunedAgent(5, evaluate_functions.capture_diff)

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)

        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__== '__main__':
    main()
