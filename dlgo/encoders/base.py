import importlib

__all__ = [
    'Encoder',
    'get_encoder_by_name',
]


class Encoder:
    # Lets you support logging or saving the name of the encoder your model is using
    def name(self):
        raise NotImplementedError()

    # Turns a Go board into numeric data
    def encoder(self, game_state):
        raise NotImplementedError()

    # Turns a Go board point into an integer index
    def encode_point(self, point):
        raise NotImplementedError()

    # Turns an integer index back into a Go board point
    def decode_point_index(self, index):
        raise NotImplementedError()

    # Number of points on the board—board width times board height
    def num_points(self):
        raise NotImplementedError()

    # Shape of the encoded board structure
    def shape(self):
        raise NotImplementedError()

# tag::encoder_by_name[]
def get_encoder_by_name(name, board_size):  # <1>
    if isinstance(board_size, int):
        board_size = (board_size, board_size)  # <2>
    module = importlib.import_module('dlgo.encoders.' + name)
    constructor = getattr(module, 'create')  # <3>
    return constructor(board_size)

# <1> We can create encoder instances by referencing their name.
# <2> If board_size is one integer, we create a square board from it.
# <3> Each encoder implementation will have to provide a "create" function that provides an instance.
# end::encoder_by_name[]
