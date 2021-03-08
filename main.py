#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import chess
import chess.engine

# Initial board
initial_board = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# Engine location
engine = chess.engine.SimpleEngine.popen_uci('./Stockfish/src/stockfish')

# OPTIMALITY SCORES
optimality_scores = {}

# CREATIVITY SCORES
creativity_scores = {}


def get_optimality_scores(fen):

    # Parse board
    board = chess.Board(fen)

    # Dict with results
    scores = {}

    # Get scores for given board
    for el in board.legal_moves:
        info = engine.analyse(board, chess.engine.Limit(time=.1), root_moves=[el])

        # Calculate score
        score = 0.0
        if(board.turn):
            score = info["score"].white().score()
        else:
            info["score"].black().score()
        score = round(score/100,2)

        # Store in dict
        scores[el.uci()] = score

    # Return scores
    return scores



#-------------------------------------
#               MAIN
#-------------------------------------
print(get_optimality_scores(initial_board))
engine.quit()