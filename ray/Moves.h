#ifndef Moves_H
#define Moves_H

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <limits>
#include "AI.h"
#include "Moves.h"
#include "Board.h"

namespace moves {

class Moves {
  public:
    Moves();
    Moves(chess::Board* t_board, int t_x, int t_y, int t_z);
    ~Moves();

    bool getCheck();

    bool checkSquare(int t_x, int t_y, int t_z, bool t_canAttack=true, bool t_canMove=true);
    void checkLine(int t_x, int t_y, int t_z, int t_moveX, int t_moveY, int t_moveZ);

    std::vector<std::pair<std::vector<int>,std::vector<int>>> pawnMoves();
    std::vector<std::pair<std::vector<int>,std::vector<int>>> rookMoves();
    std::vector<std::pair<std::vector<int>,std::vector<int>>> knightMoves();
    std::vector<std::pair<std::vector<int>,std::vector<int>>> bishopMoves();
    std::vector<std::pair<std::vector<int>,std::vector<int>>> queenMoves();
    std::vector<std::pair<std::vector<int>,std::vector<int>>> kingMoves();
    std::vector<std::pair<std::vector<int>,std::vector<int>>> unicornMoves();

  private:
    chess::Board* m_board;
    std::vector<std::pair<std::vector<int>,std::vector<int>>> m_possibleMoves;
    bool m_check = false;
    int m_x, m_y, m_z;
};
}

#endif