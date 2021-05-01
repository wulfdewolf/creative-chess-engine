#-----------------------------------------------------------------
#
#       Producing creative chess through chess-engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import abc
import chess
import chess.pgn
import os

# Chess engine class
class ChessEngine:

    def __init__(self, normal_engine):
        self.normal_engine = normal_engine

    # Prepares the engine to start a new game
    def new_game(self, color):
        self.current_position = chess.Board(chess.STARTING_FEN)
        self.game = chess.pgn.Game()
        self.optimality_count = 0
        self.creativity_counts = [0, 0, 0, 0]
        self.move_count = 0
        self.color = color

    # Makes the engine play a move, applying it to the pgn and to the position
    @abc.abstractclassmethod
    def play_move(self):
        return

    # Adds a given move to the current pgn
    def add_move_to_pgn(self, move):
        if(self.move_count == 0):
            self.game_node = self.game.add_variation(move)
        else: 
            self.game_node = self.game_node.add_variation(move)
        self.current_position.push(move)
        self.move_count += 1

    # Applies a given move to the position
    def receive_move(self, move):
        self.add_move_to_pgn(move)

    # Checks if the game is done
    def game_done(self):
        return self.current_position.is_game_over(claim_draw=True)

    # Returns the game result and the creativity counters
    def game_result(self):
        return self.current_position.result(claim_draw=True), self.creativity_counts

    # Prints the pgn of the current game to the games folder
    def pgn_to_file(self, weights, weights2):

        # Create the corresponding folder if it does not exist already
        foldername = './games/' + str(weights) + "_" + str(weights2)
        if(not(os.path.exists(foldername))):
            os.makedirs(foldername)

        # Print the game to a pgn file in the folder
        print(self.game, file=open(foldername + '/game' + str(len(os.listdir(foldername))) + ".pgn", "w"), end="\n\n")

    # Prints the counts to a file in the evaluation folder
    def counts_to_file(self, other_engine, weights, weights2):

        # Create the corresponding folder if it does not exist already
        foldername = './evaluation/' + str(weights) + "_" + str(weights2)
        if(not(os.path.exists(foldername))):
            os.makedirs(foldername)

        # Print the counts to a txt file in the folder
        print(str(
            self.optimality_count) + ' ' + str(self.move_count) + '\n' + 
            str(self.creativity_counts) + '\n\n' +
            str(other_engine.optimality_count) + ' ' + str(other_engine.move_count) + '\n' +
            str(other_engine.creativity_counts), 
            file=open(foldername + '/game' + str(len(os.listdir(foldername))) + '.txt', "w"), end="\n\n")