#------------------------------------------------
#
#           A CREATIVE CHESS ENGINE
#
#             author: Wolf De Wulf
#
#------------------------------------------------
import chess
import chess.engine
from engine import CreativeChessEngine
from optimality.optimality import get_optimality_scores
from creativity.creativity import get_creativity_scores

# Engine location
heuristics_engine = chess.engine.SimpleEngine.popen_uci('./optimality/Stockfish/src/stockfish')

#------------------------------------------------
#                    Playing
#------------------------------------------------

# Create a creative engine
creative_engine = CreativeChessEngine(chess.WHITE, heuristics_engine)

# Play against it, each time asking the player for a move in terminal
print("---------------------------------------------------------")
print("                  NEW GAME STARTED")
print("---------------------------------------------------------")
while(not(creative_engine.game_done())):

    # Let the engine play
    print("Engine move: ")
    move, hybrid_score, optimality_score, creativity_score = creative_engine.play_move()
    print(move.uci() + " with hybrid score = " + str(hybrid_score) + ", optimality score = " + str(optimality_score) + " and creativity score = " + str(creativity_score))
    print("--------------------------------------------------------------------------------")


    # Ask the player for a move
    print("Player move: ")
    move_input = str(input()).split()
    print("--------------------------------------------------------------------------------")


    # Feed the player move to the engine
    player_move = chess.Move(chess.parse_square(move_input[0]), chess.parse_square(move_input[1]))
    creative_engine.receive_move(player_move) 

# When done print the result
print("---------------------------------------------------------")
print("                  GAME IS DONE")
print("---------------------------------------------------------")
print(creative_engine.game_result())

# Stop the heuristics engine
heuristics_engine.quit()