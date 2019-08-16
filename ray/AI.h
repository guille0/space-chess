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
  public:
    AI();
    AI(long* t_array, int t_maxZ, int t_maxY, int t_maxX, int t_turn, bool t_pawn2step);
    ~AI();
    std::string boardToString();

    void setBoard(long* t_array, int t_turn);
    Board getBoard();
    // Whether the current player is in check
    bool isInCheck();
    std::vector<std::pair<std::vector<int>,std::vector<int>>> getMoves();
    std::pair<std::vector<int>,std::vector<int>> bestMove(int t_maxRecursion);
    double minimax(int t_turn, double t_biggest, double t_smallest, int t_recursionLevel=0);

  private:
    int m_maxZ, m_maxY, m_maxX;
    int m_startingTurn;
    bool m_pawn2step;
    Board m_chessboard;
    int m_maxRecursion;
};


class MinimaxBranch {
  public:
    MinimaxBranch();
    MinimaxBranch(double t_value, std::vector<int> t_piece, std::vector<int> t_move);
    ~MinimaxBranch();

    bool operator<(const MinimaxBranch& rhs) const;
    bool operator>(const MinimaxBranch& rhs) const;

    double getValue() const;
    std::vector<int> getPiece() const;
    std::vector<int> getMove() const;

  private:
    double m_value;
    std::vector<int> m_piece;
    std::vector<int> m_move;
};
}

#endif