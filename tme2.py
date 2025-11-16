import random


#LEBLEU Alexandre 21310941
#JUNG Léonard 21311189

def get_mask_one(x, y):
    """
    Retourne le masque (entier) correspondant à un pion en (x,y).
    """
    pos = x * 8 + y   
    return 1 << pos


def get_mask(l):
    """
    Retourne le masque (entier) correspondant à une liste de cases (x,y).
    """
    mask = 0
    for (x, y) in l:
        mask |= get_mask_one(x, y)   
    return mask


def rollout(game, turn=1, nb_moves=100):
    
    for _ in range(nb_moves):
    	if game.game_over()==True :
    		return game
    		
    	moves = game.valid_moves(turn)  
    	if moves:  
    		x, y = random.choice(moves)  # choix aléatoire
    		game.make_move(x, y, turn)         
    		
    	turn = -turn
    return game


def simu_mc(game , turn=1 , nb_simu=1000 , nb_moves=100):	
	results = []
	for _ in range(nb_simu):
		g = game.copy()  # copie pour ne pas modifier le jeu initial
		final_game = rollout(g, turn, nb_moves)
		results.append(final_game)
	return [e.board_to_int() for e in results]


def estime_coins(simus, nb_coins):
    
    coins_coords = [(0,0),(0,7),(7,0),(7,7)]
    mask_coins = get_mask(coins_coords)
    
    parties_filtrees = 0
    
    for sim in simus:
        bits = sim[0]  # joueur 1
        nb = bin(bits & mask_coins).count("1")
        if nb == nb_coins:
            parties_filtrees += 1

    if len(simus) == 0:
        return 0.0
    
    return parties_filtrees / len(simus)

