#-----------------------------------------------------------------
#
#       Producing creative chess through chess-engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import copy
from enum import Enum
import chess
import chess.engine
import requests
from creativity.move import Move

# Indexes for weights vector --> 
class WeightIndex(Enum):
    UNKNOWN_MOVE = 0
    LOW_WINRATE = 1
    SUBOPTIMAL_CAPTURE = 2
    SACRIFICE = 3
    OPTIMALITY = 4
  
# Chess database api-endpoint 
URL = "http://www.chessdb.cn/cdb.php?action=queryall&board="
session = requests.Session()

# Function that given a position gets all the known moves from the DB
def get_known_moves(fen):

    # Send request to DB
    result = session.get(url = URL+fen, timeout=50).text.rstrip('\x00')

    # Parse and return results
    if('|' in result):
        moves = []
        for i in result.split('|'):
            if("winrate" in i):
                moves.append(Move(i.split(',')))
        return moves
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
    elif(piece_type == 2 or piece_type == 3):
        return 3
    elif(piece_type == 4):
        return 5
    else:
        return 9

# Function that gets the captured piece type for a move that captures
def get_captured_piece_square(board, move):
    if(board.is_en_passant(move)):
        if(board.turn == chess.WHITE):
            return move.to_square - 8
        else:
            return move.to_square + 8
    else:
        return move.to_square

# Function that returns all the capture moves for a given board
def get_captures(board):
    return filter(lambda move: board.is_capture(move), board.legal_moves)

# Function that returns a deepcopy of a given board with a given move applied to it
def what_if_move_played(board, move):
    new_board = copy.deepcopy(board)
    new_board.push(move)
    return new_board

# Function that checks if a given move applied to a given board is a sacrifice
# !! a sacrifice occurs when after playing a certain move a piece can be taken by the opponent for free
def is_sacrifice(board, move):

    # Act as if the move was played
    board_after_move = what_if_move_played(board, move)
    
    # Get all the possible captures after the move has been played
    captures = get_captures(board_after_move)

    # Loop over the captures and each time check if they capture an undefended piece
    for capture in captures:
        
        # Act as if the capture was played
        board_after_capture = what_if_move_played(board_after_move, capture)

        # Check if the piece that captured can now be captured back
        if(all(i.to_square != capture.to_square for i in get_captures(board_after_capture))):
            return True

    # If no un-recapturable piece was found return false
    return False

# Given a board calculate the creativity indices of all the legal moves
def get_creativity_indices(board):

    # Dict with results
    scores = {}

    # Get the known moves from the database
    known_moves = get_known_moves(board.fen())

    # Get all of the legal moves
    legal_moves = board.legal_moves 

    # Get all of the captures
    captures = get_captures(board)

    # Get the values of all the pieces that can be captured
    capture_values = []
    for capture in captures: 

        # Get captured piece value and store it in the captures list
        capture_values.append(get_piece_value(board.piece_at(get_captured_piece_square(board, capture)).piece_type))

    # Loop over all allowed moves
    for move in legal_moves:

        # List that is re-used for each move to store the score-indices in
        score_indices = []

        # 1. The move is known and winrate < 25%
        known_move = is_known_move(move, known_moves)
        if(known_move):
            if(known_move.winrate < 25.0): 
                score_indices.append(WeightIndex.UNKNOWN_MOVE)

        # 2. The move is not known
        elif(len(known_moves) != 0):
                score_indices.append(WeightIndex.LOW_WINRATE)        

        # 3. The move captures but there is a better capture
        if(board.is_capture(move)):
            captured_piece_value = get_piece_value(board.piece_at(get_captured_piece_square(board, move)).piece_type)
            if(not(all(i <= captured_piece_value for i in captures))):
                score_indices.append(WeightIndex.SUBOPTIMAL_CAPTURE)

        # 4. The move is a sacrifice
        elif(is_sacrifice(board, move)):
            score_indices.append(WeightIndex.SACRIFICE)

        # Add the move and it's score to the dict
        scores[move] = score_indices
    
    # Return final dict
    return scores
        
