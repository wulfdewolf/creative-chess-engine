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
        self.current_position = chess.Board(chess.STARTING_FEN)
        self.game = chess.pgn.Game()
        self.move_count = 0
        self.color = color
        if(hasattr(self, 'game_node'):
            delattr(self, 'game_node')

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
            self.move_count += 1
            self.register_move(chosen_move)
            return chosen_move

        else:
            return False

    # Adds a given move to the current pgn
    def register_move(self, move):
        if(hasattr(self, 'game_node')):
            self.game_node = self.game_node.add_variation(move)
        else: 
            self.game_node = self.game.add_variation(move)
        self.current_position.push(move)

    # Checks if the game is done
    def game_done(self):
        return self.current_position.is_game_over(claim_draw=True)