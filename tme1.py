#Léonard Jung
#Alexandre Lebleu


import numpy as np
from reversi import Reversi 
from collections import defaultdict
import random

class AgentRandom:

	def __init__(self,board):
		self.board=board
		
		
	def play(self,player):
		lst = self.board.valid_moves(player)
		if len(lst)==0 :
			return  (-1,1)
		return random.choice(lst)
		
		
def count_moves_mc(nb,size,nb_simu):
    game = Reversi(size)
    player_1 = tme1.AgentRandom(board)
    player_2 = tme1.AgentRandom(board)
    d = defaultdict(int)
    for i in range(nb_simu):
        for j in range(nb):
            lst1 = game.valid_moves(player1)
            compteur[j] += len(lst1)
    		
    moyenne = sum(d.values()) / (len(d)*nb_simu)
    return moyenne
	
	
def count_config_mc(nb,size,nb_simu):
    game = Reversi(size=8)
    player1 = tme1.AgentRandom(game)
    player2 =  tme1.AgentRandom(game)
    d = defaultdict(int)
    for i in range(nb_simu):
        for j in range(nb) :
            if j%2 ==0: 
                lst1 = game.valid_moves(1)
                d[j] += len(lst1)
                x,y= player1.play(1)
                game.make_move(x,y,1)
            else:
                lst2 = game.valid_moves(-1)
                d[j] += len(lst2)
                x,y= player2.play(-1)
                game.make_move(x,y,-1)
                
    moyenne = sum(d.values()) / (len(d)*nb_simu)
    return moyenne
