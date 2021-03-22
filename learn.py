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


# Parse the input argument
N = 0
if(len(sys.argv) == 1):
    print("Please give a number of games to play!")
    exit(-1)
else:
    N = int(sys.argv[1])

# Engine location
heuristics_engine = chess.engine.SimpleEngine.popen_uci('./optimality/Stockfish/src/stockfish')

# Engine UCI options
heuristics_engine.configure({"Use NNUE": False})

#------------------------------------------------
#                    LEARNING
#------------------------------------------------

# Create two creative engines
creative_engine1 = CreativeChessEngine(heuristics_engine, [1,1,1,1,0.5], 0.1)
creative_engine2 = CreativeChessEngine(heuristics_engine, [1,1,1,1,0.5], 0.1)

# Set signal handler to print game PGN to file when ctrl-c pressed
def signal_handler(sig, frame):
    creative_engine1.pgn_to_file()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Let them play against eachother for some given amount of games
try:

    for i in range(N):

        # Prepare both engines to start a new game
        creative_engine1.new_game("game" + str(i), chess.WHITE)
        creative_engine2.new_game("game" + str(i), chess.BLACK)
    
        while(not(creative_engine1.game_done())):

            # Let engine1 play
            print("Engine1 played: ")
            move, hybrid_score, optimality_score, creativity_indices = creative_engine1.play_move()
            print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity indices = " + str([weight_index.name for weight_index in creativity_indices]))
            creative_engine2.receive_move(move)

            # If the game isn't over
            if(not(creative_engine1.game_done())):
                # Let engine2 play
                print("Engine2 played: ")
                move, hybrid_score, optimality_score, creativity_indices = creative_engine2.play_move()
                print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity indices = " + str([weight_index.name for weight_index in creativity_indices]))
                creative_engine1.receive_move(move)

        ### DEBUG: When done print the result
        print("Game is over: black - white:")
        result, creativity_counters = creative_engine1.game_result()
        print(result)
        print("With: " + str(creativity_counters))
        ###

        # Let the engines learn from the game
        creative_engine1.learn_from_game()
        creative_engine2.learn_from_game()

        # Print the learning iteration the a .csv file
        creative_engine1.print_weights()

        # Let one of the engines print the game to the games folder
        creative_engine1.pgn_to_file()

        # Swap the engines
        creative_engine1, creative_engine2 = creative_engine2, creative_engine1

    # Stop the heuristics engine
    heuristics_engine.quit()

except Exception as err:
    print(err)
    
    # Stop the heuristics engine
    heuristics_engine.quit()

    # Still print the game to file
    creative_engine1.pgn_to_file()

    # Exit the application
    sys.exit(-1)