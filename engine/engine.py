#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import abc
import chess
import chess.pgn

# Chess engine class
class ChessEngine:

    def __init__(self, name, heuristics_engine):
        self.heuristics_engine = heuristics_engine
        self.name = name

    # Prepares the engine to start a new game
    def new_game(self, game_name, color):
        self.current_position = chess.Board(chess.STARTING_FEN)
        self.game = chess.pgn.Game()
        self.game_name = game_name
        self.creativity_counters = [0, 0, 0, 0]
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
        return self.current_position.result(claim_draw=True), self.creativity_counters

    # Prints the pgn of the current game to the games folder
    def pgn_to_file(self):
        print(self.game, file=open("games/otherplay/" + ('white' if(self.color) else 'black') + '/' + self.game_name + ".pgn", "w"), end="\n\n")