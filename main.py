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

# Runs the creative system
def main(argv):

    # Engine weights: [c1, c2, c3, c4, o]
    initial_weights_w = [10, 10, 2, 2, 2]
    initial_weights_b = [11, 11, 2, 2, 2]

    # Evaluation thresholds: [c1, c2, c3, c4, o]
    thresholds_w = [0.02, 0.02, 0, 0.15, 0.8]
    thresholds_b = [0.02, 0.02, 0, 0.15, 0.8]

    # Transformational creativity added weight
    added_weight = 0.2

    # Number of games to run
    N = 200

    # Help string
    help = f"""
    Usage:  python main.py [OPTIONS]

    A creative system that produces creative chess games through chess-engine selfplay.

    Options:
    -w, --initial_weights_white    Initial weights for the white engine, default: {initial_weights_w} 
    -b, --initial_weights_black    Initial weights for the black engine, default: {initial_weights_b}
    -N                             Number of games the system should run, default: {N}
    --thresholds_white             Evaluation thresholds, default: {thresholds_w}
    --thresholds_black             Evaluation thresholds, default: {thresholds_b}
    -a, --added_weight             Theta parameter that is used to update the engine weights when a game is rejected, default: {added_weight}\n"""

    # Read optional input parameters
    try:
        opts, args = getopt.getopt(argv,"hN:w:b:a:",["initial_weights_white=","initial_weights_black=","thresholds_white=","thresholds_black=","added_weight="])
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
       elif opt == "--thresholds_white":
           thresholds_w = [float(x) for x in arg.strip('[]').split(',')]
       elif opt == "--thresholds_black":
           thresholds_b = [float(x) for x in arg.strip('[]').split(',')]
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
    ccp = CreativeChessProducer(white_engine, black_engine, thresholds_w, thresholds_b, added_weight, logger)

    try:
        # Let the engines play against each other for N games
        ccp.run(N)
    except Exception as err:
        logger.error(err)

    # Stop stockfish
    stockfish.quit()

if __name__ == "__main__":
   main(sys.argv[1:])