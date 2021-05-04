#-----------------------------------------------------------------
#
#       Producing creative chess through chess-engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import sys, getopt, signal
import logging
import chess.engine
from CCP.CreativeChessProducer import CreativeChessProducer
from engine.creative_engine import CreativeChessEngine

# Setup logger
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('main.log'))

# Help string
help = """
Usage:  python main.py [OPTIONS]

A creative system that produces creative chess games through chess-engine selfplay.

Options:
-w, --initial_weights_white    Initial weights for the white engine, default: [10,10,2,2,2]
-b, --initial_weights_black    Initial weights for the black engine, default: [10,10,2,2,2]
-N                             Number of games the system should run, default: 200
-t, --thresholds               Evaluation thresholds, default: [0.02,0.0001,0,0.05,0.4]
-a, --added_weight             Theta parameter that is added to the engine weights when a game is rejected, default: 0.2\n"""


# Runs the creative system
def main(argv):

    # Engine weights: [c1, c2, c3, c4, o]
    initial_weights_w = [10, 10, 2, 2, 2]
    initial_weights_b = [10, 10, 2, 2, 2]

    # Evaluation thresholds: [c1, c2, c3, c4, o]
    thresholds = [0.02, 0.0001, 0, 0.05, 0.4]

    # Transformational creativity added weight
    added_weight = 0.2

    # Number of games to run
    N = 200

    # Read optional input parameters
    try:
        opts, args = getopt.getopt(argv,"hNw:b:t:a:",["initial_weights_white=","initial_weights_black=","thresholds=","added_weight="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)

    for opt, arg in opts:
       if opt == '-h':
           print(help)
           sys.exit()
       elif opt == '-N':
           N = int(arg)
       elif opt in ('-w', "--initial_weights_white"):
           initial_weights_w = [float(x) for x in arg.strip('[]').split(',')]
       elif opt in ('-b', "--initial_weights_black"):
           initial_weights_b = [float(x) for x in arg.strip('[]').split(',')]
       elif opt in ("-t", "--thresholds"):
           thresholds = [float(x) for x in arg.strip('[]').split(',')]
       elif opt in ("-a", "--added_weight"):
           added_weight = float(arg)

    # Stockfish instance
    stockfish = chess.engine.SimpleEngine.popen_uci('./stockfish/binary/stockfish')

    # Signal handler to stop stockfish thread when soft kill occurs
    def signal_handler(sig, frame):

        # Stop stockfish
        stockfish.quit()

        # Exit the application
        sys.exit(0)

    # Set signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Engines
    white_engine = CreativeChessEngine(stockfish, initial_weights_w)
    black_engine = CreativeChessEngine(stockfish, initial_weights_b)

    # Creative Chess Producer
    ccp = CreativeChessProducer(white_engine, black_engine, thresholds, added_weight, logger)

    try:
        # Let the engines play against each other for N games
        ccp.run(N)
    except Exception as err:
        logger.error(err)

    # Stop stockfish
    stockfish.quit()

if __name__ == "__main__":
   main(sys.argv[1:])