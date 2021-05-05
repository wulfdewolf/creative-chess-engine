#-----------------------------------------------------------------
#
#       Producing creative chess through chess engine selfplay
#
#                       author: Wolf De Wulf
#
#-----------------------------------------------------------------
class Move:

    def __init__(self, fields):

        self.move = fields[0].split(':')[1]
        self.winrate = float(fields[4].split(':')[1].rstrip('\x00'))

    def __str__(self):
        return str(self.move) + " with winrate = " + str(self.winrate)

    def __repr__(self):
        return self.__str__()