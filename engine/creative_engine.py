#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import chess
from engine.engine import ChessEngine
from optimality.optimality import get_optimality_scores
from creativity.creativity import get_creativity_indices, WeightIndex

# Creative chess engine class
class CreativeChessEngine(ChessEngine):

    def __init__(self, name, heuristics_engine, weights, delta = 0):
        self.weights = weights
        self.delta = delta
        super(CreativeChessEngine, self).__init__(name, heuristics_engine)

    # Makes the engine play a move, applying it to the pgn and to the position
    def play_move(self):

        # Check if it is the engine's turn
        if(self.color == self.current_position.turn):

            # Get the optimality score
            optimality_scores = get_optimality_scores(self.current_position, self.heuristics_engine)

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

            # Increase the creativity counters
            for weight_index in chosen_move_creativity_indices:
                self.creativity_counters[weight_index.value] += 1

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

    # Updates the current weights by learning from the current game using an adapted version of the WoLF algorithm
    def learn_from_game(self):

        # Store the result for later use (looking it up takes time)
        self.result = self.current_position.result(claim_draw=True)
        won = self.result != ("1-0" if self.color == chess.BLACK else "0-1")
        drew = self.result == "1/2-1/2"

        ### OPTIMALITY
        if(not(won)):
            # simply add a delta if the game was lost
            self.weights[WeightIndex.OPTIMALITY.value] += self.delta
        elif(won):
            # substract a half delta if the game was won
            self.weights[WeightIndex.OPTIMALITY.value] -= self.delta/2

        ### CREATIVITY

        ## First define the delta to use: delta if we won, -delta if we lost
        if(not(won)):
            creativity_delta = -self.delta 
        elif(drew):
            creativity_delta = 1/2*self.delta 
        else:
            creativity_delta = self.delta

        ## Now add or substract the delta to the creativity weights ONLY if a corresponding move was played during the game
        for i in range(len(self.creativity_counters)):
            if(self.creativity_counters[i] > 0):
                self.weights[i] += creativity_delta 

    # Print weight iteration
    def print_weights(self):
        
        # Get game result
        won = self.result != ("1-0" if self.color == chess.BLACK else "0-1")
        drew = self.result == "1/2-1/2"

        with open('analysis/' + self.color + '_learnt.csv', 'a') as result_file:

            # Write weights
            for weight in self.weights:    
                result_file.write(str(weight) + ',')

            # Write game result
            if(drew):
                result_file.write('draw\n')
            elif(won):
                result_file.write('win\n')
            else:
                result_file.write('loss\n')