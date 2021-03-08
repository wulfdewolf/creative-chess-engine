#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import chess
import chess.engine
from optimality.optimality import get_optimality_scores
from creativity.creativity import get_creativity_scores

# Initial board
initial_board = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# Engine location
engine = chess.engine.SimpleEngine.popen_uci('./optimality/Stockfish/src/stockfish')


#------------------------------------------------
#                     MAIN
#------------------------------------------------
print(get_optimality_scores(initial_board, engine))
print(get_creativity_scores(initial_board))
engine.quit()