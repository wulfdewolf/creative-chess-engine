#-----------------------------------------------------------------
#
#       Producing creative chess through chess engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
import chess
import requests
import os

# Creative Chess Producer class
class CreativeChessProducer:

    def __init__(self, white_engine, black_engine, thresholds, added_weight, logger):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.thresholds = thresholds
        self.added_weight = added_weight
        self.logger = logger

    # Lets the two engines play a complete game
    def play_game(self):
        
        # Prepare both engines to start a new game
        self.white_engine.new_game(chess.WHITE)
        self.black_engine.new_game(chess.BLACK)
    
        while(not(self.white_engine.game_done())):

            # Let white engine play
            move = self.white_engine.play_move()
            self.black_engine.register_move(move)

            # If the game isn't over
            if(not(self.white_engine.game_done())):

                # Let black engine play
                move = self.black_engine.play_move()
                self.white_engine.register_move(move)

    # Run the CCP for a given number of games
    def run(self, N):
        
        i = 0
        while i < N:
            try: 
                self.play_game()

                # When the game is done, let the engines evaluate whether it is to be accepted or not
                evaluation_white, evaluation_black = self.evaluate_game()
                self.logger.info("-----------------------------------------")
                self.logger.info("GAME DONE, evaluating...")
                self.logger.info("white:")
                self.logger.info(str([percentage for achieved, percentage, threshold in evaluation_white]))
                self.logger.info(str(self.white_engine.weights))
                self.logger.info("black:")
                self.logger.info(str([percentage for achieved, percentage, threshold in evaluation_black]))
                self.logger.info(str(self.black_engine.weights))

                # Accept
                if((all(achieved for achieved, _, _ in evaluation_white) and evaluation_black[4][0]) or
                   (all(achieved for achieved, _, _ in evaluation_black) and evaluation_white[4][0])):

                    self.logger.info("ACCEPT")

                    # Store the accepted game
                    self.store_game()

                # Or reject and update
                else:
                    self.logger.info("REJECT")
                    self.white_engine.update_weights(evaluation_white, self.added_weight)
                    self.black_engine.update_weights(evaluation_black, self.added_weight)
                
                # Next iteration
                self.logger.info("-----------------------------------------")
                i += 1

            # If a connection error occured, act as if the game never happened
            except requests.exceptions.ConnectionError:
                self.logger.info("Connection error occurred, skipped game.")

    # Returns for both engines a list that contains for each of the engine's weights: (a boolean that indicates if they achieved their threshold, the actual percentage, the threshold itself)
    def evaluate_game(self):

        # Get move count from one of the engines (always the same)
        move_count = self.white_engine.move_count

        # Calculate evaluations
        white_evaluation = [((count / move_count) >= threshold, count / move_count, threshold)  for count, threshold in zip(self.white_engine.counts, self.thresholds)]
        black_evaluation = [((count / move_count) >= threshold, count / move_count, threshold)  for count, threshold in zip(self.black_engine.counts, self.thresholds)]
        
        return white_evaluation, black_evaluation


    # Stores an accepted game with its evaluation values to the games folder
    def store_game(self):

        # Create a folder for the game
        foldername = './games/game' + str(len(os.listdir('./games'))) 
        os.makedirs(foldername)

        # Print the game to a pgn file in the folder
        print(self.white_engine.game, file=open(foldername + "/game.pgn", "w"), end="\n\n")

        # Print the evaluation values to a txt file in the folder
        print(
            "Total number of moves: " + str(self.white_engine.move_count) + '\n' + 
            "White move counts:     " + str(self.white_engine.counts) + '\n' +
            "Black move counts:     " + str(self.black_engine.counts), 
            file=open(foldername + "/evaluation.txt", "w"), end="\n\n")