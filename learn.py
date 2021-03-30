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
from engine.creative_engine import CreativeChessEngine
from engine.heuristics_engine import HeuristicsChessEngine

# Parse the input arguments
N = 0
color_creative_engine = ""

if(len(sys.argv) != 3):
    print("python learn.py NUMBER_OF_GAMES COLOR_CREATIVE_ENGINE=BLACK|WHITE")
    exit(-1)
else:
    N = int(sys.argv[1])
    color_creative_engine = str(sys.argv[2])

# Create two heuristics engines
heuristics_engine1 = chess.engine.SimpleEngine.popen_uci('./extended-engine/binary/stockfish')
heuristics_engine2 = chess.engine.SimpleEngine.popen_uci('./extended-engine/binary/stockfish')

# Engine UCI options
heuristics_engine1.configure({"Use NNUE": False})
heuristics_engine2.configure({"Use NNUE": False})

#------------------------------------------------
#                    LEARNING
#------------------------------------------------

# Create a creative chess engine and pass it one of the heuristics engines
creative_engine = CreativeChessEngine("creative_engine", heuristics_engine1, [4,2,2,2,0.5], 0.02)

# Create a heuristics engine wrapper and pass it the other heuristics engine
heuristics_engine = HeuristicsChessEngine("heuristics_engine", heuristics_engine2)

# Signal handler to print game PGN to file when ctrl-c pressed
def signal_handler(sig, frame):

    # Print game PGN to file
    creative_engine.pgn_to_file()

    # Stop the heuristics engines
    heuristics_engine1.quit()
    heuristics_engine2.quit()

    # Exit the application
    sys.exit(0)

# Set signal handler
signal.signal(signal.SIGINT, signal_handler)

# Let them play against eachother for some given amount of games
try:

    for i in range(N):

        # Set engine places
        white_engine = creative_engine if color_creative_engine == "WHITE" else heuristics_engine
        black_engine = heuristics_engine if color_creative_engine == "WHITE" else creative_engine

        # Prepare both engines to start a new game
        white_engine.new_game("game" + str(i), chess.WHITE)
        black_engine.new_game("game" + str(i), chess.BLACK)
    
        while(not(white_engine.game_done())):

            # Let white engine play
            #print("White played: ")
            move, hybrid_score, optimality_score, creativity_indices = white_engine.play_move()
            #print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity indices = " + str([weight_index.name for weight_index in creativity_indices]))
            black_engine.receive_move(move)

            # If the game isn't over
            if(not(white_engine.game_done())):
                # Let black engine play
                #print("Black played: ")
                move, hybrid_score, optimality_score, creativity_indices = black_engine.play_move()
                #print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity indices = " + str([weight_index.name for weight_index in creativity_indices]))
                white_engine.receive_move(move)

        ### DEBUG: When done print the result
        #print("Game is over: white - black:")
        #result, creativity_counters = creative_engine.game_result()
        #print(result)
        #print("With: " + str(creativity_counters))
        ###

        # Let the creative engine learn from the game
        creative_engine.learn_from_game()

        # Print the learning iteration the a .csv file
        creative_engine.print_weights()

        # Let one of the engines print the game to the games folder
        creative_engine.pgn_to_file()

    # Stop the heuristics engines
    heuristics_engine1.quit()
    heuristics_engine2.quit()

except Exception as err:
    print(err)
    
    # Stop the heuristics engines
    heuristics_engine1.quit()
    heuristics_engine2.quit()

    # Still print the game to file
    creative_engine.pgn_to_file()

    # Exit the application
    sys.exit(-1)