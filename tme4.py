import numpy as np
import random
import tme2 
from tme2 import rollout

class  AgentFlatMCTS:
    def __init__(self,board,nb_simu=100):
        self.board=board
        self.nb_simu=nb_simu


    def play(self, turn):
        """
        Choisit le meilleur coup à jouer pour 'turn' après nb_simu simulations.
        """
        game = self.board
        legal_moves = game.valid_moves(turn)
        if not legal_moves:
            return (-1, -1)

        best_move = None
        best_ratio = -1.0

        for (row, col) in legal_moves:
            wins = 0

            for _ in range(self.nb_simu):
                # copie du jeu
                g = game.copy()
                g.make_move(row, col, turn)

                # simule la suite de la partie au hasard
                final = rollout(g, -turn,100) #100: nb_moves
                score = final.score()

                # si le joueur courant a gagné
                if (turn == 1 and score > 0) or (turn == -1 and score < 0):
                    wins += 1

            ratio = wins / self.nb_simu
            if ratio > best_ratio:
                best_ratio = ratio
                best_move = (row, col)

        return best_move






class MCTSNode:
    def __init__(self, game, player, parent=None):
        self.game = game.copy()
        self.player = player
        self.parent = parent
        self.children = {}
        self.config = game.board_to_int()
        self.visits = 0
        self.wins = 0
        self.untried_moves = game.valid_moves(player)

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def uct(self, child, K=1.4):
        if child.visits == 0:
            return float("inf")
        return (child.wins / child.visits) + np.sqrt(K * np.log(self.visits + 1) / child.visits)

    def best_move(self, K=1.4):
        best_score = -float("inf")
        best_move = None
        best_child = None
        for move, child in self.children.items():
            score = self.uct(child, K)
            if score > best_score:
                best_score = score
                best_move = move
                best_child = child
        return best_move, best_child


class AgentMCTS:
    def __init__(self, game, nb_simu=1000, K=1.4):
        self.game = game
        self.nb_simu = nb_simu
        self.K = K
        self.nodes = {}

    def play(self, player):
        # récupérer ou créer le noeud racine
        config = self.game.board_to_int()
        if config not in self.nodes:
            root = MCTSNode(self.game, player)
            self.nodes[config] = root
        else:
            root = self.nodes[config]

        # boucle principale
        for _ in range(self.nb_simu):
            node = root
            game_copy = self.game.copy()
            current_player = player

            
            while node.is_fully_expanded() and len(node.children) > 0 and not game_copy.game_over():
                move, node = node.best_move(self.K)
                game_copy.make_move(move[0], move[1], current_player)
                current_player *= -1

            
            if not node.is_fully_expanded() and not game_copy.game_over():
                move = random.choice(node.untried_moves)
                node.untried_moves.remove(move)
                game_copy.make_move(move[0], move[1], current_player)
                current_player *= -1
                child = MCTSNode(game_copy, current_player, parent=node)
                node.children[move] = child
                node = child

            #Simulation 
            final_game = rollout(game_copy, current_player, 100)
            score = final_game.score()
            if score > 0:
                result = 1
            elif score < 0:
                result = -1
            else:
                result = 0


            while node is not None:
                node.visits += 1
                if result == node.player:
                    node.wins += 1
                node = node.parent

        if not root.children:
            return (-1, -1)
        best_move = max(root.children.items(), key=lambda item: item[1].visits)[0]
        return best_move