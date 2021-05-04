#-----------------------------------------------------------------
#
#       Producing creative chess through chess-engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import chess
from engine.engine import ChessEngine
from engine.optimality.optimality import get_optimality_scores
from engine.creativity.creativity import get_creativity_indices, WeightIndex

# Normal chess engine class
class NormalChessEngine(ChessEngine):

    # Makes the engine play a move, applying it to the pgn and to the position
    def play_move(self):

        # Check if it is the engine's turn
        if(self.color == self.current_position.turn):

            # Get the optimality score
            optimality_scores = get_optimality_scores(self.current_position, self.normal_engine)
            optimality_scores = sorted(optimality_scores.items(), key=lambda item: item[1], reverse=True)

            # Get the top move
            chosen_move = optimality_scores[0][0]
            chosen_move_score = optimality_scores[0][1]

            # Play it and return it
            self.add_move_to_pgn(chosen_move)
            return chosen_move, chosen_move_score, 0, []

        else:
            return False