#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import copy
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
    result = session.get(url = URL+fen, timeout=10).text.rstrip('\x00')

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

# Given a board calculate the creativity scores of all the legal moves
def get_creativity_scores(board, move_count):

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

        # Creativity score
        score = 0

        known_move = is_known_move(move, known_moves)

        # 1. If the move is known and winrate < 20%: score +0.5
        if(known_move):
            if(known_move.winrate < 25.0): 
                score += 1

        # 2. If the move is not known: score +0.5
        elif(len(known_moves) != 0):
            score += 2

        # 3. If the move captures, if there is a better capture: score +0.5
        if(board.is_capture(move)):
            captured_piece_value = get_piece_value(board.piece_at(get_captured_piece_square(board, move)).piece_type)
            if(not(all(i <= captured_piece_value for i in captures))):
                score += 1

        # 4. If the move is a sacrifice: score +1
        elif(is_sacrifice(board, move)):
            score += 1

        # Add the move and it's score to the dict
        scores[move] = score

        # Reset score
        score = 0
    
    # Return final dict
    return scores
        
