#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <limits>
#include "AI.h"
#include "Moves.h"
#include "Board.h"

namespace chess {
// Board

Board::Board () {}

Board::Board(long* t_beginning, int t_maxZ, int t_maxY, int t_maxX, int t_turn, bool t_pawn2step)
  : m_beginning(t_beginning), m_maxZ(t_maxZ), m_maxY(t_maxY), m_maxX(t_maxX),
    m_turn(t_turn), m_pawn2step(t_pawn2step) {}

Board::~Board() {}

Board Board::copy(bool t_change_turn) {
  if (t_change_turn) {
    return Board(m_beginning, m_maxZ, m_maxY, m_maxX, m_turn*-1, m_pawn2step);
  }
  return Board(m_beginning, m_maxZ, m_maxY, m_maxX, m_turn, m_pawn2step);
}

// Getters and setters
  void Board::set(int t_x, int t_y, int t_z, int t_value) {
    m_beginning[t_x+t_y*m_maxX+t_z*(m_maxX*m_maxY)] = t_value;
  }

  int Board::get(int t_x, int t_y, int t_z) {
    return m_beginning[t_x+t_y*m_maxX+t_z*(m_maxX*m_maxY)];
  }

  int Board::getCheck() {
    return m_check;
  }

  int Board::getTurn() {
    return m_turn;
  }

  void Board::setTurn(int t_turn) {
    m_turn = t_turn;
  }

  void Board::changeTurn() {
    m_turn = m_turn*-1;
  }

  int Board::getPawn2step() {
    return m_pawn2step;
  }

  int Board::getMaxX() {
    return m_maxX;
  }

  int Board::getMaxY() {
    return m_maxY;
  }

  int Board::getMaxZ() {
    return m_maxZ;
  }

// Calculates the value of the board
double Board::getValue() {
  double boardValue = 0;

  // Count black & white pieces
  for (int z=0; z<m_maxZ; z++) {
    for (int y=0; y<m_maxY; y++) {
      for (int x=0; x<m_maxX; x++) {
        // The weights prioritize squares on the center of the board
        if (get(x,y,z) > 0) {
          boardValue += m_piecesValue[get(x,y,z)-1];
          boardValue += (addWeights(x, m_maxX) + addWeights(y, m_maxY) + addWeights(z, m_maxZ));
        } else if (get(x,y,z) < 0) {
          boardValue -= m_piecesValue[abs(get(x,y,z))-1];
          boardValue -= (addWeights(x, m_maxX) + addWeights(y, m_maxY) + addWeights(z, m_maxZ));
        }
      }
    }
  }

  return boardValue;
}
// Returns the board turned into a string for printing
std::string Board::toString() {
  std::string str = "";

  for (int z=0; z<m_maxZ; z++) {
    for (int y=0; y<m_maxY; y++) {
      for (int x=0; x<m_maxX; x++) {
        if (get(x,y,z) >= 0) {
          str += " ";
        }
        str += std::to_string(get(x,y,z));
      } str += "\n";
    } str += "\n";
  }

  str += "TURN IS: ";
  str += std::to_string(m_turn);

  return str;
}

// Returns a vector of all the possible moves a player can make
std::vector<std::pair<std::vector<int>,std::vector<int>>> Board::possibleMoves(int t_turn) {

  std::vector<std::vector<int>> pieces;

  for (int z=0; z<m_maxZ; z++) {
    for (int y=0; y<m_maxY; y++) {
      for (int x=0; x<m_maxX; x++) {
        if (get(x,y,z)*t_turn > 0) {
          pieces.push_back(std::vector<int> {x, y, z, get(x,y,z)});
  } } } }

  std::vector<std::pair<std::vector<int>,std::vector<int>>> totalMoves;

  for (auto piece : pieces) {
    // Get the moves for this piece
    std::vector<std::pair<std::vector<int>,std::vector<int>>> moves = pieceMoves(piece, t_turn);
    // Shove it into all the moves that can be made
    totalMoves.insert(std::end(totalMoves), std::begin(moves), std::end(moves));
  }
  return totalMoves;
}

// Returns all the moves a certain piece can make {{piece}, {move}}
std::vector<std::pair<std::vector<int>,std::vector<int>>>
Board::pieceMoves(std::vector<int> t_piece, int t_turn) {
  const int x = t_piece[0];
  const int y = t_piece[1];
  const int z = t_piece[2];
  // pieceType = pawn, rook, queen, etc.
  // (1,2,3,4,5,6,7,-1,-2,-3,-4,-5,-6,-7)
  const int pieceType = t_piece[3];

  std::vector<std::pair<std::vector<int>,std::vector<int>>> moves;
  moves::Moves Movement(this, t_turn, x, y, z);

  switch (abs(pieceType)) {
    case 1: {
      moves = Movement.pawnMoves();
      break;
    }
    case 2: {
      moves = Movement.rookMoves();
      break;
    }
    case 3: {
      moves = Movement.knightMoves();
      break;
    }
    case 4: {
      moves = Movement.bishopMoves();
      break;
    }
    case 5: {
      moves = Movement.queenMoves();
      break;
    }
    case 6: {
      moves = Movement.kingMoves();
      break;
    }
    case 7: {
      moves = Movement.unicornMoves();
      break;
    }
  }    
  // Whether this player has a check on the enemy on this turn
  if (m_check == false && Movement.getCheck() == true) {
      m_check = true;
  }
  return moves;
}


std::vector<std::pair<std::vector<int>,std::vector<int>>>
Board::allowedMoves(std::vector<std::pair<std::vector<int>,std::vector<int>>>
piecesAndMoves, int t_turn) {

  std::vector<std::pair<std::vector<int>,std::vector<int>>> finalMoves;

  for (auto pieceAndMove : piecesAndMoves) {
    const std::vector<int> piece = pieceAndMove.first;
    const std::vector<int> move = pieceAndMove.second;
    // Copy this board
    Board newBoard = this->copy();
    // Save the variables so we can undo the move
    const int pieceType = newBoard.get(piece[0], piece[1], piece[2]);
    const int pieceType2 = newBoard.get(move[0], move[1], move[2]);
    // Move the piece
    newBoard.set(move[0], move[1], move[2], pieceType);
    newBoard.set(piece[0], piece[1], piece[2], 0);
    // See all the possible moves for the other player, to see if he could attack the king
    newBoard.possibleMoves(t_turn*-1);
    // Reset movements
    newBoard.set(move[0], move[1], move[2], pieceType2);
    newBoard.set(piece[0], piece[1], piece[2], pieceType);

    if (newBoard.getCheck() == false) {
        finalMoves.push_back(pieceAndMove);
    }
  }
  return finalMoves;
}

// Simple weights that prioritize squares on the center of the board
double addWeights (double dim, double maxDim) {
  dim = 0.5+dim-maxDim/2;
  dim = std::abs(dim)/maxDim;
  return -dim;
}

}