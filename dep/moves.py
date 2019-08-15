from itertools import permutations
import numpy as np

from config import *

class Movement:
    def __init__(self, pawn2step, board_size=None):
        self.moves, self.attacks = [], []
        self.pawn2step = pawn2step
        self.board_size = BOARD_SIZE if board_size is None else board_size

    def check_square(self, player, array, position, only_move=False, only_eat=False):
        # Check that the square is not outside
        for dim in position:
            if dim < 0: return
        for dim, dim_max in zip(position, self.board_size):
            if dim >= dim_max: return

        # If it's empty, we can move to it
        if array[position] == 0:
            if only_eat is False:
                self.moves.append(position)
        # If it's an enemy, we can attack it
        elif player * array[position] < 0:
            if only_move is False:
                self.attacks.append(position)

    def check_line(self, player, array, position, move_x, move_y, move_z):
        # move_x, move_y, move_z can be 1, -1, 0
        # 1 if forward, -1 if backwards 0 if no motion in that dimension
        i = 0

        while True:
            i += 1
            sq = Square(x=position.x + i*move_x, y = position.y + i*move_y, z = position.z + i*move_z)

            # Break if we go outside the board
            for dim in sq:
                if dim < 0: return
            for dim, dim_max in zip(sq, self.board_size):
                if dim >= dim_max: return

            # If it's empty we can move to it
            if array[sq] == 0:
                self.moves.append(sq)
            # If there's an enemy we can attack it but nothing behind it
            elif player * array[sq] < 0:
                self.attacks.append(sq)
                return
            # If there is an ally, we can't go through them
            else:
                return

    def allowed_moves(self, player, array, position):
        '''Returns the moves and attacks a piece can perform'''
        piece = abs(array[position])
        if piece == 1: return self.pawn_moves(player, array, position)
        if piece == 2: return self.rook_moves(player, array, position)
        if piece == 3: return self.knight_moves(player, array, position)
        if piece == 4: return self.bishop_moves(player, array, position)
        if piece == 5: return self.queen_moves(player, array, position)
        if piece == 6: return self.king_moves(player, array, position)
        if piece == 7: return self.unicorn_moves(player, array, position)

    def pawn_moves(self, player, array, position):
        x, y, z = position
        # They can only move forwards (whites upwards, blacks downwards)
        self.check_square(player, array, Square(x, y+1*player, z), only_move=True)

        # If we are in the second row we can move twice (in certain gamemodes)
        if self.pawn2step is True:
            if (player == 1 and y == 1) or (player == -1 and y == self.board_size.y-2):
                # If there's nothing on the first one
                if array[x, y+1*player, z] == 0:
                    self.check_square(player, array, Square(x, y+2*player, z), only_move=True)

        self.check_square(player, array, Square(x, y, z+1*player), only_move=True)

        self.check_square(player, array, Square(x+1, y+1*player, z), only_eat=True)
        self.check_square(player, array, Square(x-1, y+1*player, z), only_eat=True)

        self.check_square(player, array, Square(x+1, y, z+1*player), only_eat=True)
        self.check_square(player, array, Square(x-1, y, z+1*player), only_eat=True)

        self.check_square(player, array, Square(x, y+1*player, z+1*player), only_eat=True)
        
        return self.moves, self.attacks
        
    def rook_moves(self, player, array, position):
        # Can move in straight lines in any dimension
        for d in (-1, 1):
            self.check_line(player, array, position, d,0,0)
            self.check_line(player, array, position, 0,d,0)
            self.check_line(player, array, position, 0,0,d)
        return self.moves, self.attacks

    def knight_moves(self, player, array, position):
        # They can move in any permutation of 2 steps one dimension, 1 step in another dimension
        perms  = list(permutations((1,2,0)))
        perms += list(permutations((1,-2,0)))
        perms += list(permutations((-1,2,0)))
        perms += list(permutations((-1,-2,0)))
        perms = list(set(perms))

        for perm in perms:
            x, y, z = [dim+dim2 for dim, dim2 in zip(position, perm)]
            self.check_square(player, array, Square(x, y, z))
        return self.moves, self.attacks

    def bishop_moves(self, player, array, position):
        # They can move as normal bishops
        self.check_line(player, array, position, 1, 1, 0)
        self.check_line(player, array, position, -1, 1, 0)
        self.check_line(player, array, position, 1, -1, 0)
        self.check_line(player, array, position, -1, -1, 0)

        # And also in a cross through the Z dimension
        self.check_line(player, array, position, 1, 0, 1)
        self.check_line(player, array, position, -1, 0, -1)
        self.check_line(player, array, position, 0, 1, 1)
        self.check_line(player, array, position, 0, -1, -1)
        return self.moves, self.attacks

    def queen_moves(self, player, array, position):
        # Combines rook, bishop and unicorn
        # Rook
        for d in (-1, 1):
            self.check_line(player, array, position, d,0,0)
            self.check_line(player, array, position, 0,d,0)
            self.check_line(player, array, position, 0,0,d)

        # Bishop
        self.check_line(player, array, position, 1, 1, 0)
        self.check_line(player, array, position, -1, 1, 0)
        self.check_line(player, array, position, 1, -1, 0)
        self.check_line(player, array, position, -1, -1, 0)

        self.check_line(player, array, position, 1, 0, 1)
        self.check_line(player, array, position, -1, 0, -1)
        self.check_line(player, array, position, 0, 1, 1)
        self.check_line(player, array, position, 0, -1, -1)

        # Unicorn
        for z in (-1, 1):
            self.check_line(player, array, position, 1,1,z)
            self.check_line(player, array, position, -1,1,z)
            self.check_line(player, array, position, 1,-1,z)
            self.check_line(player, array, position, -1,-1,z)
        return self.moves, self.attacks

    def king_moves(self, player, array, position):
        # Moves 1 step in any direction
        perms  = list(permutations((1,1,0)))
        perms += list(permutations((-1,1,0)))
        # perms += list(permutations((1,-1,0)))
        perms += list(permutations((-1,-1,0)))

        perms += list(permutations((0,1,0)))
        perms += list(permutations((-1,0,0)))
        perms = list(set(perms))

        for perm in perms:
            x, y, z = [dim+dim2 for dim, dim2 in zip(position, perm)]
            self.check_square(player, array, Square(x, y, z))
        return self.moves, self.attacks
    
    def unicorn_moves(self, player, array, position):
        # Moves in diagonals through the Z dimension
        for z in (-1, 1):
            self.check_line(player, array, position, 1,1,z)
            self.check_line(player, array, position, -1,1,z)
            self.check_line(player, array, position, 1,-1,z)
            self.check_line(player, array, position, -1,-1,z)
        return self.moves, self.attacks
