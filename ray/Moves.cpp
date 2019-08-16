#include <iostream>
#include <string>
#include <vector>
#include <vector>
#include "AI.h"
#include "Moves.h"

namespace moves {

// Just constructors
Moves::Moves() {}

Moves::Moves(chess::Board* t_board, int t_x, int t_y, int t_z)
: m_board(t_board), m_x(t_x), m_y(t_y), m_z(t_z) {}

Moves::~Moves() {}

bool Moves::getCheck() {
  return m_check;
}

// Check if we can move to a square
bool Moves::checkSquare(int t_x, int t_y, int t_z, bool can_attack, bool can_move) {
  // If the square is outside the chessboard, return false
  if (t_x<0 || t_y<0 || t_z<0 || t_x>=m_board->getMaxX() || t_y>=m_board->getMaxY() || t_z>=m_board->getMaxZ()) {
    return false;
  }

  // If there is an enemy (and we can attack with this move)
  if (m_board->getTurn()*m_board->get(t_x,t_y,t_z) < 0 && can_attack==true) {
    m_possibleMoves.push_back({std::vector<int> {m_x, m_y, m_z}, std::vector<int> {t_x,t_y,t_z}});

    // If the enemy is a king, we set CHECK to TRUE
    if (abs(m_board->get(t_x,t_y,t_z))==6) {
      m_check = true;
    }
    // Return false because we can't keep moving after attacking this piece
    return false;
  }
  // If it's empty (and we are allowed to move to this position)
  if (m_board->get(t_x,t_y,t_z) == 0 && can_move==true) {
    m_possibleMoves.push_back({std::vector<int> {m_x, m_y, m_z}, std::vector<int> {t_x,t_y,t_z}});
    return true;
  }
  return false;
}

// Check how far we can move through a line
void Moves::checkLine(int t_x, int t_y, int t_z, int t_moveX, int t_moveY, int t_moveZ) {
  // # move_x, move_y, move_z can be 1, -1, 0
  // # 1 if forward, -1 if backwards 0 if no motion in that dimension
  int i = 0;

  while (1) {
    i++;
    int goX = t_x+i*t_moveX;
    int goY = t_y+i*t_moveY;
    int goZ = t_z+i*t_moveZ;
    // If we couldn't go to this square, we can't go behind it either so just quit
    if (checkSquare(goX, goY, goZ) == false) {
      return;
    }
  }
}



std::vector<std::pair<std::vector<int>,std::vector<int>>> Moves::pawnMoves() {
  int turn = (*m_board).getTurn();

  // MOVING FORWARD (CAN'T ATTACK ON THIS MOVE)
  if (checkSquare(m_x, m_y+1*turn, m_z, false)) {
    if (m_board->getPawn2step()) {
      // If we are on the starting pawn position
      // (one step away from border and on the lowest(white)/highest(black) layer of the board)
      if (( turn == 1 && m_y == 1 && m_z == 0 )
      || ( turn == -1 && m_y == m_board->getMaxY()-2
      && m_z == m_board->getMaxZ()-1 )) {
        checkSquare(m_x, m_y+2*turn, m_z, false);
      }
    }
  }

  // Move upwards
  checkSquare(m_x, m_y, m_z+1*turn);
  

  // DIAGONALS (CAN ONLY ATTACK ON THESE)
  checkSquare(m_x+1, m_y+1*turn, m_z, true, false);
  checkSquare(m_x-1, m_y+1*turn, m_z, true, false);

  checkSquare(m_x+1, m_y, m_z+1*turn, true, false);
  checkSquare(m_x-1, m_y, m_z+1*turn, true, false);

  checkSquare(m_x, m_y+1*turn, m_z+1*turn, true, false);

  return m_possibleMoves;
}





std::vector<std::pair<std::vector<int>,std::vector<int>>> Moves::rookMoves() {
  // Straight lines in every dimension
  for (auto d : {-1, 1}) {
    checkLine(m_x,m_y,m_z, d,0,0);
    checkLine(m_x,m_y,m_z, 0,d,0);
    checkLine(m_x,m_y,m_z, 0,0,d);
  }
  return m_possibleMoves;
}

std::vector<std::pair<std::vector<int>,std::vector<int>>> Moves::knightMoves() {
  for (auto d : {-1, 1}) {
    for (auto d2 : {-2, 2}) {
      // Diagonal steps in x,y axis
      checkSquare(m_x+d, m_y+d2, m_z);
      checkSquare(m_x+d2, m_y+d, m_z);
      // Diagonal steps in x,z axis
      checkSquare(m_x+d, m_y, m_z+d2);
      checkSquare(m_x+d2, m_y, m_z+d);
      // Diagonal steps in y,z axis
      checkSquare(m_x, m_y+d, m_z+d2);
      checkSquare(m_x, m_y+d2, m_z+d);
    }
  }
  return m_possibleMoves;
}



std::vector<std::pair<std::vector<int>,std::vector<int>>> Moves::bishopMoves() {
  for (auto d : {-1, 1}) {
    // Diagonals like a normal bishop
    checkLine(m_x, m_y, m_z, d,d*-1,0);
    checkLine(m_x, m_y, m_z, d,d,0);
    // And straight lines through the Z dimension
    checkLine(m_x, m_y, m_z, d,0,d);
    checkLine(m_x, m_y, m_z, 0,d,d);
  }
  return m_possibleMoves;
}

std::vector<std::pair<std::vector<int>,std::vector<int>>> Moves::queenMoves() {
  // Rook+Bishop+Unicorn
  for (auto d : {-1, 1}) {
    // Rook moves
    checkLine(m_x, m_y, m_z, d,0,0);
    checkLine(m_x, m_y, m_z, 0,d,0);
    checkLine(m_x, m_y, m_z, 0,0,d);

    // Bishop moves
    checkLine(m_x, m_y, m_z, d,d*-1,0);
    checkLine(m_x, m_y, m_z, d,d,0);
    checkLine(m_x, m_y, m_z, d,0,d);
    checkLine(m_x, m_y, m_z, 0,d,d);

    // Unicorn moves
    checkLine(m_x, m_y, m_z, 1,1,d);
    checkLine(m_x, m_y, m_z, -1,1,d);
    checkLine(m_x, m_y, m_z, 1,-1,d);
    checkLine(m_x, m_y, m_z, -1,-1,d);
  }
  return m_possibleMoves;
}

std::vector<std::pair<std::vector<int>,std::vector<int>>> Moves::kingMoves() {
  for (auto d : {-1, 1}) {
    // 1 Step in every direction
    checkSquare(m_x+d, m_y, m_z);
    checkSquare(m_x, m_y+d, m_z);
    checkSquare(m_x, m_y, m_z+d);
    for (auto d2 : {-1, 1}) {
      // Diagonal steps in x,y axis
      checkSquare(m_x+d, m_y+d2, m_z);
      // Diagonal steps in x,z axis
      checkSquare(m_x+d, m_y, m_z+d2);
      // Diagonal steps in y,z axis
      checkSquare(m_x, m_y+d, m_z+d2);
      for (auto d3 : {-1, 1}) {
        // Superdiagonal steps (x,y,z)
        checkSquare(m_x+d, m_y+d2, m_z+d3);
      }
    }
  }
  return m_possibleMoves;
}


std::vector<std::pair<std::vector<int>,std::vector<int>>> Moves::unicornMoves() {
  for (auto d : {-1, 1}) {
    // Diagonals through the Z dimension
    checkLine(m_x, m_y, m_z, 1,1,d);
    checkLine(m_x, m_y, m_z, -1,1,d);
    checkLine(m_x, m_y, m_z, 1,-1,d);
    checkLine(m_x, m_y, m_z, -1,-1,d);
  }
  return m_possibleMoves;
}


}
