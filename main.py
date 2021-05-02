#-----------------------------------------------------------------
#
#       Producing creative chess through chess-engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import sys
import signal
import chess
import chess.engine
from engine.creative_engine import CreativeChessEngine
from engine.normal_engine import NormalChessEngine

# Parse the input arguments
N = 0

if(len(sys.argv) != 2):
    print("python main.py NUMBER_OF_GAMES")
    exit(-1)
else:
    N = int(sys.argv[1])


# Create a Stockfish instance
stockfish = chess.engine.SimpleEngine.popen_uci('./extended-engine/binary/stockfish')

# Engine UCI options
stockfish.configure({"Use NNUE": False})

# Define the weights that the engines will use
weights = [2, 2, 2, 2, 2]
weights2 = [2, 2, 2, 2, 2]

# Create a creative chess engine and pass it the Stockfish instance
creative_engine = CreativeChessEngine(stockfish, weights)

# Create another creative chess engine and pass it the Stockfish instance
creative_engine2 = CreativeChessEngine(stockfish, weights2)

# Signal handler to print game PGN to file when ctrl-c pressed
def signal_handler(sig, frame):

    # Print game PGN to file
    creative_engine.pgn_to_file(weights, weights2)

    # Stop stockfish
    stockfish.quit()

    # Exit the application
    sys.exit(0)

# Set signal handler
signal.signal(signal.SIGINT, signal_handler)

# Let them play against eachother for some given amount of games
try:

    for i in range(0, N):

        # Set engine places
        white_engine = creative_engine
        black_engine = creative_engine2

        # Prepare both engines to start a new game
        white_engine.new_game(chess.WHITE)
        black_engine.new_game(chess.BLACK)
    
        while(not(white_engine.game_done())):

            # Let white engine play
            move, hybrid_score, optimality_score, creativity_indices = white_engine.play_move()
            black_engine.receive_move(move)

            # If the game isn't over
            if(not(white_engine.game_done())):
                # Let black engine play
                move, hybrid_score, optimality_score, creativity_indices = black_engine.play_move()
                white_engine.receive_move(move)

        # When the game is done, let the engines evaluate whether it is to be accepted or not
        optimality_threshold = 0.5
        creativity_thresholds = [0, 0, 0, 0.2]
        print("GAME DONE, evaluating...")
        print("engine 1:")
        optimality_ok, creativity_oks, creativity_all_ok = creative_engine.evaluate_current_game(optimality_threshold, creativity_thresholds)
        print("engine 2:")
        optimality_ok2, creativity_oks2, creativity_all_ok2 = creative_engine2.evaluate_current_game(optimality_threshold, creativity_thresholds)

        # Accept or reject and update
        if(optimality_ok and creativity_all_ok and optimality_ok2 and creativity_all_ok2):
            print("ACCEPT")

            # Let one of the engines print the creative game to the games folder
            creative_engine.pgn_to_file(weights, weights2)

            # Let one of the engines print both engines' counts to the evaluation folder
            creative_engine.counts_to_file(creative_engine2, weights, weights2)

        else:
            print("REJECT")
            creative_engine.update_weights(optimality_ok, creativity_oks, creativity_all_ok, 0.2)
            creative_engine2.update_weights(optimality_ok2, creativity_oks2, creativity_all_ok2, 0.2)

    # Stop stockfish
    stockfish.quit()

except Exception as err:
    print(err)
    
    # Stop stockfish
    stockfish.quit()

    # Still print the game to file
    creative_engine.pgn_to_file(weights, weights2)

    # Exit the application
    sys.exit(-1)
