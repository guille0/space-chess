#ifndef Board_H
#define Board_H

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <limits>
#include "AI.h"
#include "Moves.h"
#include "Board.h"


namespace chess {

class Board {
  public:
    Board();
    Board(long* t_beginning, int t_maxZ, int t_maxY, int t_maxX, int t_turn, bool t_pawn2step);
    ~Board();

    Board copy(bool t_change_turn=true);

    void set(int t_x, int t_y, int t_z, int t_value);
    int get(int t_x, int t_y, int t_z);

    // Calculates value of the board on every call
    double getValue();

    int getMaxX();
    int getMaxY();
    int getMaxZ();
    int getCheck();
    int getTurn();
    int getPawn2step();

    void setTurn(int t);
    void changeTurn();

    // Checking for moves
    std::vector<std::pair<std::vector<int>,std::vector<int>>>
    possibleMoves(int t_turn);
    // Moves a piece can make in theory
    std::vector<std::pair<std::vector<int>,std::vector<int>>>
    pieceMoves(std::vector<int> t_piece, int t_turn);
    // Moves we can actually make without putting our own king in check
    std::vector<std::pair<std::vector<int>,std::vector<int>>>
    allowedMoves(std::vector<std::pair<std::vector<int>,std::vector<int>>> t_moves, int t_turn);

    // Other
    std::string toString();

  private: 
    long* m_beginning;
    int m_maxZ, m_maxY, m_maxX;
    int m_turn;
    bool m_pawn2step;
    int m_piecesValue[7] = {10, 50, 30, 30, 90, 900, 30};
    // Whether there is a check on this board against player 'turn'
    bool m_check = false;
};

double addWeights(double dim, double maxDim);

}

#endif