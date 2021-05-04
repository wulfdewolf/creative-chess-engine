#-----------------------------------------------------------------
#
#       Producing creative chess through chess-engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import sys, getopt
import logging
import signal
import chess
import chess.engine
from engine.creative_engine import CreativeChessEngine
from engine.normal_engine import NormalChessEngine

# Setup logger
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('main.log'))


# Runs the creative system
def main(argv):

    # Define the weights that the engines will use: [c1, c2, c3, c4, o]
    initial_weights_w = [10, 10, 2, 2, 2]
    initial_weights_b = [10, 10, 2, 2, 2]

    # Define the evaluation thresholds: [c1, c2, c3, c4, o]
    thresholds = [0.02, 0.0001, 0, 0.05, 0.4]

    # Define the transformational creativity added weight
    added_weight = 0.2

    # Define the number of games to run
    N = 200

    # Read optional input parameters
    try:
        opts, args = getopt.getopt(argv,"hNw:b:t:a:",["initial_weights_white=","initial_weights_black=","thresholds=","added_weight="])
    except getopt.GetoptError:
        print('python main.py -ww [1,2,3,4,5] -wb [1,2,3,4,5] -t [1,2,3,4,5] -aw 1')
        sys.exit(2)

    for opt, arg in opts:
       if opt == '-h':
           print('python main.py -ww [1,2,3,4,5] -wb [1,2,3,4,5] -t [1,2,3,4,5] -aw 1')
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

    # Create a Stockfish instance
    stockfish = chess.engine.SimpleEngine.popen_uci('./extended-engine/binary/stockfish')
    
    # Create the creative chess engine that will play as white and pass it the Stockfish instance
    white_engine = CreativeChessEngine(stockfish, initial_weights_w)

    # Create the creative chess engine that will play as black and pass it the Stockfish instance
    black_engine = CreativeChessEngine(stockfish, initial_weights_b)

    # Signal handler to print game PGN to file when ctrl-c pressed
    def signal_handler(sig, frame):

        # Print game PGN to file
        white_engine.pgn_to_file(black_engine)

        # Stop stockfish
        stockfish.quit()

        # Exit the application
        sys.exit(0)

    # Set signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Let the engines play against each other for N games
    try:
        for i in range(0, N):

            # Prepare both engines to start a new game
            white_engine.new_game(chess.WHITE)
            black_engine.new_game(chess.BLACK)
    
            while(not(white_engine.game_done())):

                # Let white engine play
                move = white_engine.play_move()
                black_engine.receive_move(move)

                # If the game isn't over
                if(not(white_engine.game_done())):
                    # Let black engine play
                    move = black_engine.play_move()
                    white_engine.receive_move(move)

            # When the game is done, let the engines evaluate whether it is to be accepted or not
            evaluation_white = white_engine.evaluate_game(thresholds)
            evaluation_black = black_engine.evaluate_game(thresholds)
            logger.info("GAME DONE, evaluating...")
            logger.info("white:")
            logger.info(str([percentage for achieved, percentage, threshold in evaluation_white]))
            logger.info(str(white_engine.weights))
            logger.info("black:")
            logger.info(str([percentage for achieved, percentage, threshold in evaluation_black]))
            logger.info(str(black_engine.weights))

            # Accept
            if((all(achieved for achieved, _, _ in evaluation_white) and evaluation_black[4][0]) or
               (all(achieved for achieved, _, _ in evaluation_black) and evaluation_white[4][0])):
                logger.info("ACCEPT")

                # Let one of the engines print the creative game to the games folder
                white_engine.pgn_to_file(black_engine)

                # Let one of the engines print both engines' counts to the evaluation folder
                white_engine.counts_to_file(black_engine)

            # Or reject and update
            else:
                logger.info("REJECT")
                white_engine.update_weights(evaluation_white, added_weight)
                black_engine.update_weights(evaluation_black, added_weight)

        # Stop stockfish
        stockfish.quit()

    except Exception as err:
        logger.error(err)
    
        # Stop stockfish
        stockfish.quit()

        # Still print the game to file
        white_engine.pgn_to_file(black_engine)

        # Exit the application
        sys.exit(-1)


if __name__ == "__main__":
   main(sys.argv[1:])