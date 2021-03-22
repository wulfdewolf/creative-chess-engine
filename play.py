#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import sys
import signal
import chess
import chess.engine
from engine import CreativeChessEngine

# Engine location
heuristics_engine = chess.engine.SimpleEngine.popen_uci('./optimality/Stockfish/src/stockfish')

#------------------------------------------------
#                    Playing
#------------------------------------------------

# Create a creative engine
creative_engine = CreativeChessEngine("engine", heuristics_engine, [1,1,1,1,1])

# Prepare it to start a new game
creative_engine.new_game("PlayerGame", chess.WHITE)

# Set signal handler to print game PGN to file when ctrl-c pressed
def signal_handler(sig, frame):
    creative_engine.pgn_to_file()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Engine UCI options
heuristics_engine.configure({"Use NNUE": False})

# Play against it, each time asking the player for a move in terminal
print("---------------------------------------------------------")
print("                  NEW GAME STARTED")
print("---------------------------------------------------------")

try:

    while(not(creative_engine.game_done())):

        # Let the engine play
        print("Engine move: ")
        move, hybrid_score, optimality_score, creativity_indices = creative_engine.play_move()
        print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity indices = " + str([weight_index.name for weight_index in creativity_indices]))
        print("--------------------------------------------------------------------------------")


        # Ask the player for a move
        print("Player move: ")
        move_input = str(input()).split()
        print("--------------------------------------------------------------------------------")


        # Feed the player move to the engine
        player_move = chess.Move(chess.parse_square(move_input[0]), chess.parse_square(move_input[1]))
        creative_engine.receive_move(player_move) 

    # When done print the result
    print("---------------------------------------------------------")
    print("                  GAME IS DONE")
    print("---------------------------------------------------------")
    print("black - white:")
    print(creative_engine.game_result())

    # Let the engine print the game to the games folder
    creative_engine.pgn_to_file()

    # Stop the heuristics engine
    heuristics_engine.quit()

except Exception as err:
    print(err)

    # Stop the heuristics engine
    heuristics_engine.quit()

    # Still print the game to file
    creative_engine.pgn_to_file()

    # Exit the application
    sys.exit(-1)