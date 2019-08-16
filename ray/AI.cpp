#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <limits>
#include "AI.h"
#include "Moves.h"
#include "Board.h"

namespace chess {
AI::AI () {}

AI::AI (long* t_array, int t_maxZ, int t_maxY, int t_maxX, int t_turn, bool t_pawn2step)
: m_maxZ(t_maxZ), m_maxY(t_maxY), m_maxX(t_maxX), m_startingTurn(t_turn), m_pawn2step(t_pawn2step){
  m_chessboard = Board(t_array, t_maxZ, t_maxY, t_maxX, t_turn, t_pawn2step);
}

AI::~AI () {}

void AI::setBoard(long* t_array, int t_turn) {
  m_chessboard = Board(t_array, m_maxZ, m_maxY, m_maxX, t_turn, m_pawn2step);
}

// Getters and setters
  Board AI::getBoard() {
      return m_chessboard;
  }

std::string AI::boardToString() {
  return m_chessboard.toString();
}

std::vector<std::pair<std::vector<int>,std::vector<int>>> AI::getMoves() {
  std::vector<std::pair<std::vector<int>,std::vector<int>>> moves;
  // get every single move we could make (including moves that would put our king in danger)
  moves = m_chessboard.possibleMoves(m_chessboard.getTurn());
  // from those, exclude the ones that would put our king in danger
  moves = m_chessboard.allowedMoves(moves, m_chessboard.getTurn());

  return moves;
}

bool AI::isInCheck() {
  // Check all possible moves for the  (which sets the check variable)
  m_chessboard.possibleMoves(m_startingTurn*-1);
  return m_chessboard.getCheck();
}

std::pair<std::vector<int>,std::vector<int>> AI::bestMove(int t_maxRecursion) {
  m_maxRecursion = t_maxRecursion;

  MinimaxBranch bestIdea =
  MinimaxBranch(std::numeric_limits<double>::max()*m_chessboard.getTurn()*-1, {0,0,0}, {0,0,0});

  std::vector<std::pair<std::vector<int>,std::vector<int>>> moves = getMoves();

  for (auto pieceAndMove : moves) {
    const std::vector<int> piece = pieceAndMove.first;
    const std::vector<int> move = pieceAndMove.second;

    const int type = m_chessboard.get(piece[0], piece[1], piece[2]);
    const int type2 = m_chessboard.get(move[0], move[1], move[2]);
    m_chessboard.set(move[0], move[1], move[2], type);
    m_chessboard.set(piece[0], piece[1], piece[2], 0);
    const double value = minimax(m_chessboard.getTurn()*-1,
      -std::numeric_limits<double>::max(), std::numeric_limits<double>::max(), 0);
    m_chessboard.set(move[0], move[1], move[2], type2);
    m_chessboard.set(piece[0], piece[1], piece[2], type);
    
    // If this one is better than the last best one
    const MinimaxBranch thisIdea = MinimaxBranch(value, piece, move);
    if ((m_chessboard.getTurn() == -1 && thisIdea < bestIdea)
    || (m_chessboard.getTurn() == 1 && thisIdea > bestIdea)) {
      bestIdea = thisIdea;
    }
  }
  return std::pair<std::vector<int>,std::vector<int>> {bestIdea.getPiece(), bestIdea.getMove()};
}

double AI::minimax(int t_turn, double t_biggest, double t_smallest, int t_recursionLevel) {
  // Get the moves for this board and player
  const std::vector<std::pair<std::vector<int>,std::vector<int>>> moves
  = m_chessboard.allowedMoves(m_chessboard.possibleMoves(t_turn), t_turn);

  if (moves.empty()) {
    m_chessboard.allowedMoves(m_chessboard.possibleMoves(t_turn*-1), t_turn*-1);
    // This player cannot move, let's see if he is in check (checkmate) or not (draw)
    if (m_chessboard.getCheck()) {
      return (9999-t_recursionLevel*5)*t_turn*-1;
    } else {
      return 0;
    }
  } else if (t_recursionLevel >= m_maxRecursion) {
    return m_chessboard.getValue();

  } else if (t_turn == 1) {
    double maxEval = -std::numeric_limits<double>::max();

    for (auto pieceAndMove : moves) {
      const std::vector<int> piece = pieceAndMove.first;
      const std::vector<int> move = pieceAndMove.second;

      const int type = m_chessboard.get(piece[0], piece[1], piece[2]);
      const int type2 = m_chessboard.get(move[0], move[1], move[2]);
      m_chessboard.set(move[0], move[1], move[2], type);
      m_chessboard.set(piece[0], piece[1], piece[2], 0);
      const double value = minimax(t_turn*-1, t_biggest, t_smallest, t_recursionLevel+1);
      m_chessboard.set(move[0], move[1], move[2], type2);
      m_chessboard.set(piece[0], piece[1], piece[2], type);
      // Alpha-beta pruning
      maxEval = std::max(maxEval, value);
      t_biggest = std::max(t_biggest, value);
      if (t_smallest <= t_biggest) {
        break;
      }
    }
    return maxEval;
  } else {
    double minEval = std::numeric_limits<double>::max();

    for (auto pieceAndMove : moves) {
      const std::vector<int> piece = pieceAndMove.first;
      const std::vector<int> move = pieceAndMove.second;

      const int type = m_chessboard.get(piece[0], piece[1], piece[2]);
      const int type2 = m_chessboard.get(move[0], move[1], move[2]);
      m_chessboard.set(move[0], move[1], move[2], type);
      m_chessboard.set(piece[0], piece[1], piece[2], 0);
      const double value = minimax(t_turn*-1, t_biggest, t_smallest, t_recursionLevel+1);
      m_chessboard.set(move[0], move[1], move[2], type2);
      m_chessboard.set(piece[0], piece[1], piece[2], type);
      // Alpha-beta pruning
      minEval = std::min(minEval, value);
      t_smallest = std::min(t_smallest, value);
      if (t_smallest <= t_biggest) {
        break;
      }
    }
    return minEval;
  }
}

// MinimaxBranch

  MinimaxBranch::MinimaxBranch() {}
  MinimaxBranch::MinimaxBranch(double t_value, std::vector<int> t_piece, std::vector<int> t_move)
  : m_value(t_value), m_piece(t_piece), m_move(t_move) {}

  MinimaxBranch::~MinimaxBranch () {}

  // Comparing
    bool MinimaxBranch::operator<(const MinimaxBranch& rhs) const {
      return m_value < rhs.m_value;
    }
    bool MinimaxBranch::operator>(const MinimaxBranch& rhs) const {
      return m_value > rhs.m_value;
    }

  // Getters and setters
    double MinimaxBranch::getValue() const {
      return m_value;
    }
    std::vector<int> MinimaxBranch::getPiece() const {
      return m_piece;
    }
    std::vector<int> MinimaxBranch::getMove() const {
      return m_move;
    }

}
