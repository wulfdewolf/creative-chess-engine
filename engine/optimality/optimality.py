#-----------------------------------------------------------------
#
#       Producing creative chess through chess engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
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
            if(score_info.white().is_mate()):
                score -= score_info.white().mate() * 100
        else:
            score = score_info.black().score(mate_score=1000000)
            if(score_info.black().is_mate()):
                score -= score_info.black().mate() * 100
        score = round(score/100,2)

        # Store in dict
        scores[el] = score

    # Return scores
    return scores