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
    result = str(requests.get(url = URL+fen).text)

    # Parse and return
    return [Move(i.split(',')) for i in result.split('|')]


# Given a board calculate the creativity scores of all the legal moves
def get_creativity_scores(fen):
    return get_known_moves(fen)