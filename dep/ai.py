import numpy as np
import time

from moves import Movement
from config import *


class AiMove:

    def __init__(self):
        # Pawn, Rook, Knight, Bishop, Queen, King, Unicorn
        self.values = [10, 50, 30, 30, 90, 900, 30]
        self.max_recursion = 2

    def best_move(self, board, valid_moves, turn, max_recursion=None):
        # NOTE
        # Takes too long if there's a lot of posibilities
        # because Python is slow and the algorithm isn't well optimized.
        # It works well on small boards/few pieces/puzzles
        # but a Raumschach board is a bit too much for it.
        print(f'{len(valid_moves)} moves')
        if max_recursion is None:
            if len(valid_moves) > 40:
                self.max_recursion = 0
            elif len(valid_moves) > 15:
                self.max_recursion = 1
            elif len(valid_moves) > 10:
                self.max_recursion = 2
        else:
            self.max_recursion = max_recursion
 
        best_move = MoveIdea(np.inf*turn*-1, None, None)
        for piece, move in valid_moves:
            # Creates a board where this move has been made
            idea_board = np.copy(board)
            self.move_pieces(idea_board, piece, move)
            # Checks how much the board would benefit us with this move
            # (edit self.max_recursion for going deeper)
            this_move = MoveIdea(self.minimax(idea_board, turn*-1, -np.inf, np.inf, 0), piece, move)
            # Compares every board against eachother and comes out with the best move
            best_move = max((best_move, this_move), key=lambda x: x.value*turn)

        return best_move.piece, best_move.move


    def minimax(self, board, turn, biggest, smallest, recursion_level=0):
        '''Minimax algorithm with alpha-beta pruning'''

        # Sleep for faster fps but lower AI performance
        time.sleep(0.001)

        _, valid_moves = self.get_valid_moves(board, turn)

        # If the player can't move, it could be a checkmate or a draw
        if not valid_moves:
            if self.king_check(board, turn*-1):
                # If its a checkmate, we give it super high priority for the AI
                return -(9999-recursion_level*5)*turn
            else:
                # If its a draw, we give it 0 priority,
                # so if we're losing a draw could be the best choice
                return 0

        elif recursion_level >= self.max_recursion:
            # Actually analyzes the board
            node_value = self.board_value(board)
            return node_value

        elif turn == 1:
            maxEval = -np.inf
            for piece, move in valid_moves:
                # Creates a new board where the best move for this player is made
                idea_board = np.copy(board)
                self.move_pieces(idea_board, piece, move)
                # Check the value of that board
                value = self.minimax(idea_board, turn*-1, biggest, smallest, recursion_level+1)
                maxEval = max(maxEval, value)
                biggest = max(biggest, value)
                # See minimax alpha-beta
                if smallest <= biggest:
                    break
            return maxEval
        else:
            minEval = np.inf
            for piece, move in valid_moves:
                # Creates a new board where the best move for this player is made
                idea_board = np.copy(board)
                self.move_pieces(idea_board, piece, move)
                # Check the value of that board
                value = self.minimax(idea_board, turn*-1, biggest, smallest, recursion_level+1)
                minEval = min(minEval, value)
                smallest = min(smallest, value)
                # See minimax alpha-beta
                if smallest <= biggest:
                    break
            return minEval


    def move_pieces(self, array, one, other):
        # Move one to other's position
        array[other.x, other.y, other.z] = array[one.x, one.y, one.z]
        # Replace one's position with empty
        array[one.x, one.y, one.z] = 0


    def board_value(self, board):

        # Added weight to every square in the board,
        # making positions in the center more valuable.
        # Not perfect, should be a specific set of weights for each piece
        # but this way it gets automatically generated for boards of any shape
        def weights(dim, max_dim):
            dim = 0.5+dim-max_dim/2
            return abs(dim)/max_dim*10
        
        xx, yy, zz = BOARD_SIZE

        whites = 0
        blacks = 0

        for x in range(xx):
            for y in range(yy):
                for z in range(zz):
                    value = board[x, y, z]
                    if value > 0:
                        whites += self.values[abs(value)-1]
                        whites += 5 - (weights(x, xx) + weights(y, yy) + weights(z, zz))
                    elif value < 0:
                        blacks += self.values[abs(value)-1]
                        blacks += 5 - (weights(x, xx) + weights(y, yy) + weights(z, zz))

        total = whites - blacks

        return total


    def get_valid_moves(self, board, turn, only_attacks=False, pawn2step=None, board_size=None):
        all_moves = []
        valid_moves = []
        if pawn2step is None:
            pawn2step = PAWN_2STEP
        if board_size is None:
            board_size = BOARD_SIZE
        max_x, max_y, max_z = board_size



        # Get all the moves the player can make
        for z in range(max_z):
            for y in range(max_y):
                for x in range(max_x):
                    if board[x,y,z] * turn > 0:
                        # Get moves for the current player
                        moves, attacks = Movement(pawn2step, board_size).allowed_moves(turn, board, Square(x,y,z))
                        if only_attacks is True:
                            all_moves.append((Square(x,y,z), attacks))
                        else:
                            all_moves.append((Square(x,y,z), moves+attacks))

        # Check how many moves would not put the king in danger
        for piece, moves in all_moves:
            for move in moves:
                # load original board
                idea_board = np.copy(board)
                # do the move on the new array
                self.move_pieces(idea_board, piece, move)
                # See if the other player could attack the king after this move
                if self.king_check(idea_board, turn*-1, pawn2step, board_size) is False:
                    valid_moves.append((piece, move))

        # If there are moves that don't put the king in danger, there's no checkmate
        if valid_moves:
            return False, valid_moves
        else:
            return True, None


    def king_check(self, array, turn, pawn2step=None, board_size=None):
        if pawn2step is None:
            pawn2step = PAWN_2STEP
        if board_size is None:
            board_size = BOARD_SIZE
        max_x, max_y, max_z = board_size
        # Gets every possible move by the player to see if a king is under check
        for z in range(max_z):
            for y in range(max_y):
                for x in range(max_x):
                    if array[x,y,z] * turn > 0:
                        _, attacks = Movement(pawn2step, board_size).allowed_moves(turn, array, Square(x,y,z))
                        for attack in attacks:
                            if abs(array[attack.x, attack.y, attack.z]) == 6:
                                return True
        return False


class MoveIdea:
    def __init__(self, value, piece, move):
        self.value = value
        self.piece = piece
        self.move = move
    
    def __lt__(self, other):
        if self.value < other.value:
            return True

    def __gt__(self, other):
        if self.value > other.value:
            return True
    
    def __eq__(self, other):
        if self.value == other.value:
            return True

