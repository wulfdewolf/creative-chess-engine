#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import chess
import chess.engine


# Given a board calculate the creativity scores of all the legal moves
def get_creativity_scores(fen, engine):

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