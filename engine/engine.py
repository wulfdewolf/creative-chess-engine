#-----------------------------------------------------------------
#
#       Producing creative chess through chess engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import abc
import chess
import chess.pgn

# Chess engine class
class ChessEngine:

    def __init__(self, inner_engine):
        self.inner_engine = inner_engine

    # Prepares the engine to start a new game
    def new_game(self, color):
        self.color = color

    # Makes the engine play a move, applying it to the pgn and to the position
    def play_move(self, current_position):

        # Check if it is the engine's turn
        if(self.color == current_position.turn):

            # Get the optimality score
            optimality_scores = get_optimality_scores(current_position, self.normal_engine)
            optimality_scores = sorted(optimality_scores.items(), key=lambda item: item[1], reverse=True)

            # Get the top move
            chosen_move = optimality_scores[0][0]
            chosen_move_score = optimality_scores[0][1]

            # Play it and return it
            return chosen_move, [4]

        else:
            return False