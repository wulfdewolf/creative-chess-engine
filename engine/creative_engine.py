#-----------------------------------------------------------------
#
#       Producing creative chess through chess-engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import chess
from engine.engine import ChessEngine
from optimality.optimality import get_optimality_scores
from creativity.creativity import get_creativity_indices, WeightIndex

# Creative chess engine class
class CreativeChessEngine(ChessEngine):

    def __init__(self, normal_engine, weights):
        self.weights = weights
        super(CreativeChessEngine, self).__init__(normal_engine)

    # Makes the engine play a move, applying it to the pgn and to the position
    def play_move(self):

        # Check if it is the engine's turn
        if(self.color == self.current_position.turn):

            # Get the optimality scores
            optimality_scores = get_optimality_scores(self.current_position, self.normal_engine)

            # Get the optimal move string
            optimal_move = max(optimality_scores, key = optimality_scores.get)

            # Get creativity indices
            creativity_indices = get_creativity_indices(self.current_position)

            # Merge the scores using the weights and sort
            hybrid_scores = self.get_hybrid_scores(optimality_scores, creativity_indices)
            hybrid_scores = sorted(hybrid_scores.items(), key=lambda item: item[1], reverse=True)

            # Get the top move
            chosen_move = hybrid_scores[0][0]
            chosen_move_score = hybrid_scores[0][1]
            chosen_move_optimality_score = optimality_scores[chosen_move]
            chosen_move_creativity_indices = creativity_indices[chosen_move]

            # Increase the optimality counter
            if(optimal_move == chosen_move):
                self.optimality_count += 1

            # Increase the creativity counters
            for weight_index in chosen_move_creativity_indices:
                self.creativity_counts[weight_index.value] += 1

            # Play it and return it
            self.add_move_to_pgn(chosen_move)
            return chosen_move, chosen_move_score, chosen_move_optimality_score, chosen_move_creativity_indices

        else:
            return False

    # Calculats the hybrid scores from the optimality and creativity scores
    def get_hybrid_scores(self, optimality_scores, creativity_indices):

        merged_scores = {}
        hybrid_scores = {}
        
        # 1. Merge the two dicts together to get: (key, (O_score, C_indices))
        for move in list(optimality_scores) + list(creativity_indices):

            # The move is in both dicts
            if(move in creativity_indices and move in optimality_scores):
                merged_scores[move] = (optimality_scores[move], creativity_indices[move])

            # The move is in one of the dicts
            elif(move in creativity_indices):
                merged_scores[move] = (0.0, creativity_indices[move])

            else:
                merged_scores[move] = (optimality_scores[move], 0.0)
            
        # 2. Loop over the merged scores and calculate the hybrid scores
        for move, score_and_indices in merged_scores.items():
            
            # Split up the cell of scores
            optimality_score, creativity_indices = score_and_indices

            # Calculate hybrid scores, start by adding optimality score
            hybrid_scores[move] = self.weights[WeightIndex.OPTIMALITY.value]*optimality_score 

            # Loop over creativity indices to add creativity weights
            for creativity_indice in creativity_indices:
                hybrid_scores[move] += self.weights[creativity_indice.value]

        # Return the hybrid scores
        return hybrid_scores