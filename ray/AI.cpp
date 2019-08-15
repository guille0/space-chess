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
  moves = m_chessboard.possibleMoves();
  // from those, exclude the ones that would put our king in danger
  moves = m_chessboard.allowedMoves(moves);

  return moves;
}

bool AI::isInCheck() {
  // Make a copy of chessboard
  Board newBoard = m_chessboard.copy();
  // Check all possible moves for the enemy
  newBoard.possibleMoves();
  return newBoard.getCheck();
}

std::pair<std::vector<int>,std::vector<int>> AI::bestMove(int t_maxRecursion) {
  m_maxRecursion = t_maxRecursion;

  std::vector<int> piece = {0,0,0};
  std::vector<int> move = {0,0,0};

  int worst;
  if (m_chessboard.getTurn() == -1) {
    worst = std::numeric_limits<int>::max();
  } else {
    worst = std::numeric_limits<int>::min();
  }

  MinimaxBranch best_idea = MinimaxBranch(worst, piece, move);

  std::vector<std::pair<std::vector<int>,std::vector<int>>> possibleMoves = getMoves();

  for (auto piece_and_move : possibleMoves) {
    piece = piece_and_move.first;
    move = piece_and_move.second;

    Board new_board = m_chessboard.copy(false);
    // Get which kind of piece it is, since it's not specified
    const int type = new_board.get(piece[0], piece[1], piece[2]);
    const int type2 = new_board.get(move[0], move[1], move[2]);
    new_board.set(move[0], move[1], move[2], type);
    new_board.set(piece[0], piece[1], piece[2], 0);
    // See all the possible moves for the other player, to see if he could attack the king
    const int value = minimax(new_board, std::numeric_limits<int>::min(), std::numeric_limits<int>::max(), 0);
    const MinimaxBranch this_idea = MinimaxBranch(value, piece, move);
    new_board.set(move[0], move[1], move[2], type2);
    new_board.set(piece[0], piece[1], piece[2], type);
    
    if ((m_chessboard.getTurn() == -1 && this_idea < best_idea)
    || (m_chessboard.getTurn() == 1 && this_idea > best_idea)) {
        best_idea = this_idea;
      }
  }

  return std::pair<std::vector<int>,std::vector<int>> {best_idea.getPiece(), best_idea.getMove()};

}

int AI::minimax(Board t_board, int t_biggest, int t_smallest, int t_recursion_level) {
  // std::vector<std::pair<std::vector<int>,std::vector<int>>> moves;

  t_board.changeTurn();
  // Get the moves for this board and player
  const std::vector<std::pair<std::vector<int>,std::vector<int>>> moves = t_board.allowedMoves(t_board.possibleMoves());

  if (moves.empty()) {
      // The enemy cannot move, let's see if he is in check with my weird backwards functions
      // that make me have to change the turn
      t_board.changeTurn();
      t_board.allowedMoves(t_board.possibleMoves());

      if (t_board.getCheck()) {
          std::cout << "Found a checkmate\n";
          return (9999-t_recursion_level*5)*t_board.getTurn();
      } else {
          // If it's a draw, give it 0 priority
          return 0;
      }
  } else if (t_recursion_level >= m_maxRecursion){
      return t_board.getValue();

  } else if (t_board.getTurn() == 1) {
      int max_eval = std::numeric_limits<int>::min();
      for (auto piece_and_move : moves) {
          const std::vector<int> piece = piece_and_move.first;
          const std::vector<int> move = piece_and_move.second;

          Board new_board = t_board.copy(false);
          const int type = m_chessboard.get(piece[0], piece[1], piece[2]);
          const int type2 = m_chessboard.get(move[0], move[1], move[2]);
          m_chessboard.set(move[0], move[1], move[2], type);
          m_chessboard.set(piece[0], piece[1], piece[2], 0);
          const int value = minimax(new_board, t_biggest, t_smallest, t_recursion_level+1);
          m_chessboard.set(move[0], move[1], move[2], type2);
          m_chessboard.set(piece[0], piece[1], piece[2], type);
          max_eval = std::max(max_eval, value);
          t_biggest = std::max(t_biggest, value);
          if (t_smallest <= t_biggest) {
              break;
          }
      }
      return max_eval;
  } else {
      int min_eval = std::numeric_limits<int>::max();
      for (auto piece_and_move : moves) {
          const std::vector<int> piece = piece_and_move.first;
          const std::vector<int> move = piece_and_move.second;

          Board new_board = t_board.copy(false);
          const int type = m_chessboard.get(piece[0], piece[1], piece[2]);
          const int type2 = m_chessboard.get(move[0], move[1], move[2]);
          m_chessboard.set(move[0], move[1], move[2], type);
          m_chessboard.set(piece[0], piece[1], piece[2], 0);
          const int value = minimax(new_board, t_biggest, t_smallest, t_recursion_level+1);
          m_chessboard.set(move[0], move[1], move[2], type2);
          m_chessboard.set(piece[0], piece[1], piece[2], type);

          min_eval = std::min(min_eval, value);
          t_smallest = std::min(t_smallest, value);
          if (t_smallest <= t_biggest) {
              break;
          }
      }
      return min_eval;
  }
}

// MinimaxBranch

  MinimaxBranch::MinimaxBranch() {}
  MinimaxBranch::MinimaxBranch(int t_value, std::vector<int> t_piece, std::vector<int> t_move)
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
    // int MinimaxBranch::getValue() {
    //   return m_value;
    // }
    int MinimaxBranch::getValue() const {
      return m_value;
    }
    std::vector<int> MinimaxBranch::getPiece() const {
      return m_piece;
    }
    std::vector<int> MinimaxBranch::getMove() const {
      return m_move;
    }

}
