import random
import numpy as np

class AgentRandom:
    """
        Un agent aléatoire qui joue au jeu.
    """
    def __init__(self,board):
        self.board = board

    def play(self,player):
        lst = self.board.valid_moves(player)
        if len(lst) ==0:
            return (-1,-1)
        return random.choice(lst)

