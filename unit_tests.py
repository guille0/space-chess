import unittest
import numpy as np

from ai import AiMove
from config import *


class TestMovement(unittest.TestCase):

    def test_raumschach_movement(self):
        '''Tests movement for all pieces in the base raumschach board'''
        raumschach = np.transpose(np.array(RAUMSCHACH_BOARD, dtype=np.int8), (2, 1, 0))

        _, moves = AiMove().get_valid_moves(board=raumschach, turn=1, pawn2step=RAUMSCHACH_PAWN_2STEP, board_size=RAUMSCHACH_SIZE)

        expected_moves = [(Square(x=1, y=0, z=0), Square(x=1, y=1, z=2)), (Square(x=1, y=0, z=0), Square(x=1, y=2, z=1)), (Square(x=1, y=0, z=0), Square(x=2, y=2, z=0)), (Square(x=1, y=0, z=0), Square(x=0, y=0, z=2)), (Square(x=1, y=0, z=0), Square(x=0, y=2, z=0)), (Square(x=1, y=0, z=0), Square(x=2, y=0, z=2)), (Square(x=3, y=0, z=0), Square(x=3, y=1, z=2)), (Square(x=3, y=0, z=0), Square(x=3, y=2, z=1)), (Square(x=3, y=0, z=0), Square(x=4, y=2, z=0)), (Square(x=3, y=0, z=0), Square(x=2, y=0, z=2)), (Square(x=3, y=0, z=0), Square(x=2, y=2, z=0)), (Square(x=3, y=0, z=0), Square(x=4, y=0, z=2)), (Square(x=0, y=1, z=0), Square(x=0, y=2, z=0)), (Square(x=1, y=1, z=0), Square(x=1, y=2, z=0)), (Square(x=2, y=1, z=0), Square(x=2, y=2, z=0)), (Square(x=3, y=1, z=0), Square(x=3, y=2, z=0)), (Square(x=4, y=1, z=0), Square(x=4, y=2, z=0)), (Square(x=0, y=0, z=1), Square(x=1, y=0, z=2)), (Square(x=0, y=0, z=1), Square(x=2, y=0, z=3)), (Square(x=0, y=0, z=1), Square(x=3, y=0, z=4)), (Square(x=0, y=0, z=1), Square(x=0, y=1, z=2)), (Square(x=0, y=0, z=1), Square(x=0, y=2, z=3)), (Square(x=0, y=0, z=1), Square(x=0, y=3, z=4)), (Square(x=1, y=0, z=1), Square(x=2, y=1, z=2)), (Square(x=1, y=0, z=1), Square(x=3, y=2, z=3)), (Square(x=1, y=0, z=1), Square(x=0, y=1, z=2)), (Square(x=1, y=0, z=1), Square(x=4, y=3, z=4)), (Square(x=2, y=0, z=1), Square(x=2, y=0, z=2)), (Square(x=2, y=0, z=1), Square(x=2, y=0, z=3)), (Square(x=2, y=0, z=1), Square(x=2, y=0, z=4)), (Square(x=2, y=0, z=1), Square(x=3, y=0, z=2)), (Square(x=2, y=0, z=1), Square(x=4, y=0, z=3)), (Square(x=2, y=0, z=1), Square(x=2, y=1, z=2)), (Square(x=2, y=0, z=1), Square(x=2, y=2, z=3)), (Square(x=2, y=0, z=1), Square(x=3, y=1, z=2)), (Square(x=2, y=0, z=1), Square(x=4, y=2, z=3)), (Square(x=2, y=0, z=1), Square(x=1, y=1, z=2)), (Square(x=2, y=0, z=1), Square(x=0, y=2, z=3)), (Square(x=2, y=0, z=1), Square(x=2, y=3, z=4)), (Square(x=3, y=0, z=1), Square(x=4, y=1, z=2)), (Square(x=3, y=0, z=1), Square(x=2, y=1, z=2)), (Square(x=3, y=0, z=1), Square(x=1, y=2, z=3)), (Square(x=3, y=0, z=1), Square(x=0, y=3, z=4)), (Square(x=4, y=0, z=1), Square(x=4, y=1, z=2)), (Square(x=4, y=0, z=1), Square(x=4, y=2, z=3)), (Square(x=4, y=0, z=1), Square(x=4, y=3, z=4)), (Square(x=0, y=1, z=1), Square(x=0, y=2, z=1)), (Square(x=0, y=1, z=1), Square(x=0, y=1, z=2)), (Square(x=1, y=1, z=1), Square(x=1, y=2, z=1)), (Square(x=1, y=1, z=1), Square(x=1, y=1, z=2)), (Square(x=2, y=1, z=1), Square(x=2, y=2, z=1)), (Square(x=2, y=1, z=1), Square(x=2, y=1, z=2)), (Square(x=3, y=1, z=1), Square(x=3, y=2, z=1)), (Square(x=3, y=1, z=1), Square(x=3, y=1, z=2)), (Square(x=4, y=1, z=1), Square(x=4, y=2, z=1)), (Square(x=4, y=1, z=1), Square(x=4, y=1, z=2))]
    
        for move in moves:
            msg = f'''
            Unexpected move found:
            {PIECES[raumschach[move[0]]]} trying to move to {PIECES[raumschach[move[1]]]}
            {move[1].x-move[0].x} in x dimension
            {move[1].y-move[0].y} in y dimension
            {move[1].z-move[0].z} in z dimension
            from {move[0].x, move[0].y, move[0].z} to {move[1].x, move[1].y, move[1].z}.
            This move should not be allowed.'''
            self.assertIn(move, expected_moves, msg=msg)

        for move in expected_moves:
            msg = f'''
            Expected move not found:
            {PIECES[raumschach[move[0]]]} should be able to move to {PIECES[raumschach[move[1]]]}
            {move[1].x-move[0].x} in x dimension
            {move[1].y-move[0].y} in y dimension
            {move[1].z-move[0].z} in z dimension
            from {move[0].x, move[0].y, move[0].z} to {move[1].x, move[1].y, move[1].z}.
            This move should be allowed.'''
            self.assertIn(move, moves, msg=msg)
        
        if len(moves) != len(expected_moves):
            print('WARNING: The amount of moves was different than expected. Maybe moves.py is generating duplicate moves?')
            print(f'Expected {len(expected_moves)}, got {len(moves)}.')

        if len(moves) != len((set(moves))):
            print('WARNING: moves.py seems to be generating duplicate moves. It should still work fine.')
            print(f'Got {len(moves)-len((set(moves)))} duplicated moves.')


    def test_classic_movement(self):
        '''Tests movement for all pieces in the base classic board'''
        classic = np.transpose(np.array(CLASSIC_BOARD, dtype=np.int8), (2, 1, 0))

        _, moves = AiMove().get_valid_moves(board=classic, turn=1, pawn2step=CLASSIC_PAWN_2STEP, board_size=CLASSIC_SIZE)

        expected_moves = [(Square(x=1, y=0, z=0), Square(x=2, y=2, z=0)), (Square(x=1, y=0, z=0), Square(x=0, y=2, z=0)), (Square(x=6, y=0, z=0), Square(x=7, y=2, z=0)), (Square(x=6, y=0, z=0), Square(x=5, y=2, z=0)), (Square(x=0, y=1, z=0), Square(x=0, y=2, z=0)), (Square(x=0, y=1, z=0), Square(x=0, y=3, z=0)), (Square(x=1, y=1, z=0), Square(x=1, y=2, z=0)), (Square(x=1, y=1, z=0), Square(x=1, y=3, z=0)), (Square(x=2, y=1, z=0), Square(x=2, y=2, z=0)), (Square(x=2, y=1, z=0), Square(x=2, y=3, z=0)), (Square(x=3, y=1, z=0), Square(x=3, y=2, z=0)), (Square(x=3, y=1, z=0), Square(x=3, y=3, z=0)), (Square(x=4, y=1, z=0), Square(x=4, y=2, z=0)), (Square(x=4, y=1, z=0), Square(x=4, y=3, z=0)), (Square(x=5, y=1, z=0), Square(x=5, y=2, z=0)), (Square(x=5, y=1, z=0), Square(x=5, y=3, z=0)), (Square(x=6, y=1, z=0), Square(x=6, y=2, z=0)), (Square(x=6, y=1, z=0), Square(x=6, y=3, z=0)), (Square(x=7, y=1, z=0), Square(x=7, y=2, z=0)), (Square(x=7, y=1, z=0), Square(x=7, y=3, z=0))]

        for move in moves:
            msg = f'''
            Unexpected move found:
            {PIECES[classic[move[0]]]} trying to move to {PIECES[classic[move[1]]]}
            {move[1].x-move[0].x} in x dimension
            {move[1].y-move[0].y} in y dimension
            {move[1].z-move[0].z} in z dimension
            from {move[0].x, move[0].y, move[0].z} to {move[1].x, move[1].y, move[1].z}.
            This move should not be allowed.'''
            self.assertIn(move, expected_moves, msg=msg)

        for move in expected_moves:
            msg = f'''
            Expected move not found:
            {PIECES[classic[move[0]]]} should be able to move to {PIECES[classic[move[1]]]}
            {move[1].x-move[0].x} in x dimension
            {move[1].y-move[0].y} in y dimension
            {move[1].z-move[0].z} in z dimension
            from {move[0].x, move[0].y, move[0].z} to {move[1].x, move[1].y, move[1].z}.
            This move should be allowed.'''
            self.assertIn(move, moves, msg=msg)
        
        if len(moves) != len(expected_moves):
            print('WARNING: The amount of moves was different than expected. Maybe moves.py is generating duplicate moves?')
            print(f'Expected {len(expected_moves)}, got {len(moves)}.')

        if len(moves) != len((set(moves))):
            print('WARNING: moves.py seems to be generating duplicate moves. It should still work fine.')
            print(f'Got {len(moves)-len((set(moves)))} duplicated moves.')



if __name__ == '__main__':
    unittest.main()
    
