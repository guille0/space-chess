from libcpp.string cimport string
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.pair cimport pair
cdef extern from "AI.cpp" namespace "chess":
    pass
cdef extern from "Moves.cpp" namespace "chess":
    pass
cdef extern from "Board.cpp" namespace "chess":
    pass
cdef extern from "AI.h" namespace "chess":
    cdef cppclass AI:
        AI() except +
        AI(long*, int, int, int, int, bool) except +

        vector[pair[vector[int],vector[int]]] getMoves()
        pair[vector[int],vector[int]] bestMove(int)

        bool isInCheck()
        void setBoard(long*, int)

        string boardToString()
