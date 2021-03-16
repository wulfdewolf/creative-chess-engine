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
session = requests.Session()

# Function that given a position gets all the known moves from the DB
def get_known_moves(fen):

    # Send request to DB
    result = session.get(url = URL+fen).text.rstrip('\x00')

    # Parse and return results
    if('|' in result):
        return [Move(i.split(',')) for i in result.split('|')]
    else:
        return []


# Function that gets a move from the known moves or returns false if it isn't known
def is_known_move(move, known_moves):
    for known_move in known_moves:
        if(move.uci() == known_move.move):
            return known_move
    return False

# Function that gets the value of a piece
def get_piece_value(piece_type):
    if(piece_type == 1):
        return 1
    elif(piece_type == 2 | piece_type == 3):
        return 3
    elif(piece_type == 4):
        return 5
    else:
        return 9


# Given a board calculate the creativity scores of all the legal moves
def get_creativity_scores(board):

    # Dict with results
    scores = {}

    # List of possile capture values
    captures = []

    # Get the known moves from the database
    known_moves = get_known_moves(board.fen())

    # Get all of the legal moves
    legal_moves = board.legal_moves 

    # Get the values of all the pieces that can be captured
    for move in legal_moves: 
        if(board.is_capture(move)):

            # Get captured piece value and store it in the captures list
            captured_piece_type = board.piece_at(move.to_square).piece_type
            captures.append(get_piece_value(captured_piece_type))


    # Loop over all allowed moves
    for move in legal_moves:

        # Creativity score
        score = 0

        known_move = is_known_move(move, known_moves)

        # 1. If the move is known and winrate < 20%: score +0.5
        if(known_move):
            if(known_move.winrate < 25.0): 
                score += 0.5

        # 2. If the move is not known: score +0.5
        else:
            score += 0.5

        # 3. If the move captures, if there is a better capture: score +0.5
        if(board.is_capture(move)):
            captured_piece_value = get_piece_value(board.piece_at(move.to_square).piece_type)
            if(not(all(i <= captured_piece_value for i in captures))):
                score += 0.5

        # Add the move and it's score to the dict
        scores[move] = score

        # Reset score
        score = 0
    
    # Return final dict
    return scores
        
