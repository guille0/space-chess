import numpy as np
from config import *


class Piece(object):
    def __init__(self, player, position, showbase=None):
        self.showbase = showbase
        self.player = player
        self.position = position

        self.obj = showbase.loader.loadModel(self.model)
        self.obj.reparent_to(showbase.anchor)
        self.obj.setScale(SCALE*PIECE_SCALE)
        self.obj.setColor((1, 1, 1, 1))

        if player == -1:
            self.obj.setTexture(showbase.texture_black)
            self.obj.setHpr(0,90,0)
        else:
            self.obj.setTexture(showbase.texture_white)
            self.obj.setHpr(180,90,0)
        self.move(position)

    def move(self, position):
        self.position = position
        self.obj.setPos(square_position(*position, BOARD_SIZE))


class Pawn(Piece):
    model = MODEL_PAWN

    def __repr__(self):
        return 'P'

class Rook(Piece):
    model = MODEL_ROOK

    def __repr__(self):
        return 'R'

class Knight(Piece):
    model = MODEL_KNIGHT

    def __repr__(self):
        return 'N'

class Bishop(Piece):
    model = MODEL_BISHOP

    def __repr__(self):
        return 'B'

class Queen(Piece):
    model = MODEL_QUEEN

    def __repr__(self):
        return 'Q'

class King(Piece):
    model = MODEL_KING

    def __repr__(self):
        return 'K'

class Unicorn(Piece):
    model = MODEL_UNICORN

    def __repr__(self):
        return 'U'
