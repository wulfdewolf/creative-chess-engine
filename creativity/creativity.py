#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import chess
import chess.engine
import requests
from creativity.move import Move
  
# Chess database api-endpoint 
URL = "http://www.chessdb.cn/cdb.php?action=queryall&board="

# Function that given a position gets all the known moves from the DB
def get_known_moves(fen):

    # Send request to DB
    result = requests.get(url = URL+fen).text.rstrip('\x00')

    # Parse and return results
    if(result == "unknown"):
        return []
    else:
        return [Move(i.split(',')) for i in result.split('|')]


# Function that gets a move from the known moves or returns false if it isn't known
def is_known_move(move, known_moves):
    for known_move in known_moves:
        if(move.uci() == known_move.move):
            return known_move
    return False


# Given a board calculate the creativity scores of all the legal moves
def get_creativity_scores(board):

    # Dict with results
    scores = {}

    # Get the known moves from the database
    known_moves = get_known_moves(board.fen())

    # Get all of the legal moves
    legal_moves = board.legal_moves 
    print(known_moves)

    # Loop over all allowed moves
    for move in legal_moves:

        # Creativity score
        score = 0

        known_move = is_known_move(move, known_moves)

        # 1. If the move is known and winrate < 20%: score +0.5
        if(known_move):
            print("got here")
            if(known_move.winrate < 25.0): 
                score += 1

        # 2. If the move is not known: score +0.5
        else:
            score += 1

        # Add the move and it's score to the dict
        scores[move] = score

        # Reset score
        score = 0
    
    # Return final dict
    return scores
        
