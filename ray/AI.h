#ifndef ChessAI_H
#define ChessAI_H

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <limits>
#include "AI.h"
#include "Moves.h"
#include "Board.h"

namespace chess {

class AI {
    private:
        Board m_chessboard;
        int m_startingTurn;
        bool m_pawn2step;
        int m_maxZ, m_maxY, m_maxX;
        int m_maxRecursion;

    public:
        AI();
        AI(long* t_array, int t_maxZ, int t_maxY, int t_maxX, int t_turn, bool t_pawn2step);
        ~AI();

        void setBoard(long* t_array, int t_turn);
        Board getBoard();

        std::string boardToString();

        std::vector<std::pair<std::vector<int>,std::vector<int>>> getMoves();
        // Whether the current player is in check
        bool isInCheck();

        std::pair<std::vector<int>,std::vector<int>> bestMove(int t_max_recursion);

        int minimax(Board t_board, int t_biggest, int t_smallest, int t_recursion_level=0);
};


class MinimaxBranch {
    private:
        int m_value;
        std::vector<int> m_piece;
        std::vector<int> m_move;

    public:
        MinimaxBranch();
        MinimaxBranch(int t_value, std::vector<int> t_piece, std::vector<int> t_move);
        ~MinimaxBranch();

        bool operator<(const MinimaxBranch& rhs) const;
        bool operator>(const MinimaxBranch& rhs) const;

        // void setValue(int t_value);
        int getValue() const;
        // int getValue() const;
        std::vector<int> getPiece() const;
        std::vector<int> getMove() const;
        
};
}

#endif