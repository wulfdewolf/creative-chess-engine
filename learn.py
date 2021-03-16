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
from optimality.optimality import get_optimality_scores
from creativity.creativity import get_creativity_scores


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
creative_engine1 = CreativeChessEngine(chess.WHITE, heuristics_engine)
creative_engine2 = CreativeChessEngine(chess.BLACK, heuristics_engine)

# Set signal handler to print game PGN to file when ctrl-c pressed
def signal_handler(sig, frame):
    creative_engine1.pgn_to_file()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Let them play against eachother for some given amount of games
for i in range(N):
    
    while(not(creative_engine1.game_done())):

        # Let engine1 play
        print("Engine1 played: ")
        move, hybrid_score, optimality_score, creativity_score = creative_engine1.play_move()
        print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity score = " + str(creativity_score))
        creative_engine2.receive_move(move)

        # Let engine2 play
        print("Engine2 played: ")
        move, hybrid_score, optimality_score, creativity_score = creative_engine2.play_move()
        print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity score = " + str(creativity_score))
        creative_engine1.receive_move(move)

    # When done print the result
    print("Game is over: black - white:")
    print(creative_engine1.game_result())

# Stop the heuristics engine
heuristics_engine.quit()