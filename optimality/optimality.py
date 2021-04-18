#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import chess
import chess.engine


# Given a board and an engine calculate the optimality scores of all the legal moves
def get_optimality_scores(board, engine):

    # Dict with results
    scores = {}

    # Get scores for given board
    for el in board.legal_moves:
        score_info = engine.analyse(board, chess.engine.Limit(time=.01), root_moves=[el])["score"]

        # Calculate score
        score = 0.0
        if(board.turn):
            score = score_info.white().score(mate_score=1000000)
        else:
            score = score_info.black().score(mate_score=1000000)
        score = round(score/100,2)

        # Store in dict
        scores[el] = score

    # Return scores
    return scores