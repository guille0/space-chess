# distutils: language = c++

from Ray cimport *

import cython
import numpy as np
cimport numpy as np

from libcpp cimport bool

# The class the user will be able to access
cdef class Chess_AI:
    '''np.ndarray[long, ndim=3, mode="c"], turn (-1 or 1), pawn_2step (bool)'''

    # Holds the C++ object in this variable
    cdef AI c_ai  

    def __cinit__(self, np.ndarray[long, ndim=3, mode="c"] input, int turn, bool pawn_2step):
        # Array, turn, pawn_2step
        max_x, max_y, max_z = input.shape[0], input.shape[1], input.shape[2]

        self.c_ai = AI(&input[0,0,0], max_x, max_y, max_z, turn, pawn_2step)

    def print_board(self):
        string = self.c_ai.boardToString().decode('ascii')
        print(string)
    
    def get_moves(self):
        return self.c_ai.getMoves()
    
    def is_in_check(self):
        return self.c_ai.isInCheck()

    def set_board(self, np.ndarray[long, ndim=3, mode="c"] input, int turn):
        self.c_ai.setBoard(&input[0,0,0], turn)

    def best_move(self, int max_recursion):
        return self.c_ai.bestMove(max_recursion)

