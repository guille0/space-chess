from panda3d.core import LPoint3

# EDIT GAMEMODE AT THE BOTTOM (CHESS VARIANTS)

# COLORS (for the squares)
BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
HIGHLIGHT = (0, 1, 1, 1)
HIGHLIGHT_MOVE = (0, 1, 0, 1)
HIGHLIGHT_ATTACK = (1, 0, 0, 1)

# SCALE (for the 3D representation)
SCALE = 0.5
PIECE_SCALE = 0.3
BOARD_HEIGHT = 1.5

# MODELS
MODEL_PAWN = "models/pawn.obj"
MODEL_ROOK = "models/rook.obj"
MODEL_KNIGHT = "models/knight.obj"
MODEL_BISHOP = "models/bishop.obj"
MODEL_QUEEN = "models/queen.obj"
MODEL_KING = "models/king.obj"
MODEL_UNICORN = "models/unicorn.obj"

# MODEL TEXTURES
TEXTURE_WHITE = "models/light_wood.jpg"
TEXTURE_BLACK = "models/dark_wood.jpg"

# HELPER FUNCTIONS

def square_position(x, y, z, board_size):
    # Gives the 3d position of a square based on x, y, z
    xx, yy, zz = board_size
    x = (x - (3.5/8)*xx) * SCALE
    y = (y - (3.5/8)*yy) * SCALE
    z = z*BOARD_HEIGHT * SCALE

    return LPoint3(x, y, z)

def square_color(x, y, z):
    # Checks whether a square should be black or white
    if (x+y+z) % 2 == 0:
        return BLACK
    else:
        return WHITE

# BOARDS
# 1 = Pawn
# 2 = Rook
# 3 = Knight
# 4 = Bishop
# 5 = Queen
# 6 = King
# 7 = Unicorn
# + = white
# - = black
# First array = lowest level
# Highest part of the array = front (white pieces)

PIECES = {
        0: 'empty space',
        -1: 'black pawn',
        -2: 'black rook',
        -3: 'black knight',
        -4: 'black bishop',
        -5: 'black queen',
        -6: 'black king',
        -7: 'black unicorn',
        1: 'white pawn',
        2: 'white rook',
        3: 'white knight',
        4: 'white bishop',
        5: 'white queen',
        6: 'white king',
        7: 'white unicorn',
}

RAUMSCHACH_PAWN_2STEP = False
RAUMSCHACH_BOARD = [
         [
          [ 2, 3, 6, 3, 2],
          [ 1, 1, 1, 1, 1],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
         ],
         [
          [ 4, 7, 5, 7, 4],
          [ 1, 1, 1, 1, 1],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
         ],
         [
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
         ],
         [
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [-1,-1,-1,-1,-1],
          [-4,-7,-5,-7,-4],
         ],
         [
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [-1,-1,-1,-1,-1],
          [-2,-3,-6,-3,-2],
         ],
        ]

SMALL_RAUMSCHACH_PAWN_2STEP = False
SMALL_RAUMSCHACH_BOARD = [
         [
          [ 2, 4, 6, 4, 2],
          [ 3, 1, 1, 1, 3],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
         ],
         [
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
         ],
         [
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0],
          [-3,-1,-1,-1,-3],
          [-2,-4,-6,-4,-2],
         ],
        ]

CARD_PAWN_2STEP = True
CARD_BOARD = [
         [
          [ 2, 5, 6, 2],
          [ 1, 1, 1, 1],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
         ],
         [
          [ 4, 3, 3, 4],
          [ 1, 1, 1, 1],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [-1,-1,-1,-1],
          [-4,-3,-3,-4],
         ],
         [
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [ 0, 0, 0, 0],
          [-1,-1,-1,-1],
          [-2,-5,-6,-2],
         ],
        ]

CLASSIC_PAWN_2STEP = True
CLASSIC_BOARD = [
         [
          [ 2, 3, 4, 5, 6, 4, 3, 2],
          [ 1, 1, 1, 1, 1, 1, 1, 1],
          [ 0, 0, 0, 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0, 0, 0, 0],
          [ 0, 0, 0, 0, 0, 0, 0, 0],
          [-1,-1,-1,-1,-1,-1,-1,-1],
          [-2,-3,-4,-5,-6,-4,-3,-2],
         ],
        ]


# NOTE: PAWN_2STEP is whether the pawn can take 2 steps if it's on the second line (bool)
RAUMSCHACH = [RAUMSCHACH_BOARD, RAUMSCHACH_PAWN_2STEP]
SMALL_RAUMSCHACH = [SMALL_RAUMSCHACH_BOARD, SMALL_RAUMSCHACH_PAWN_2STEP]
CARD = [CARD_BOARD, CARD_PAWN_2STEP]
CLASSIC = [CLASSIC_BOARD, CLASSIC_PAWN_2STEP]


TEST_PAWN_2STEP = True
TEST_BOARD = [
         [
          [ 0, 1, 6, 0],
          [ 0, 0, 0, 0],
          [ 0, 0,-2,-2],
          [ 0, 0, 0, 0],
         ],
        ]

TEST = [TEST_BOARD, TEST_PAWN_2STEP]

# Edit gamemode here
GAMEMODE = SMALL_RAUMSCHACH

# Edit players here
HUMANS = [-1]
AIS = [1]

BOARD, PAWN_2STEP = GAMEMODE
BOARD_SIZE = (len(BOARD[0][0]), len(BOARD[0]), len(BOARD))
TEST = False
