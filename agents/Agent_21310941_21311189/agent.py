import random
import time
import numpy as np
from bitreversi import BitboardReversi

def rollout(game, to_move, max_moves=100):
    """ Simulation aléatoire jusqu’à la fin. """
    g = game.copy()
    cur = to_move
    for _ in range(max_moves):
        if g.game_over():
            break
        moves = g.valid_moves(cur)
        if moves:
            r, c = random.choice(moves)
            g.make_move(r, c, cur)
        cur = -cur
    s = g.score()
    if s > 0:
        return 1
    elif s < 0:
        return -1
    else:
        return 0


class MCTSNode:
    def __init__(self, game, to_move, parent=None, move_from_parent=None):
        self.game = game
        self.to_move = to_move
        self.parent = parent
        self.move_from_parent = move_from_parent
        self.children = {}
        self.visits = 0
        self.wins = 0
        self.untried_moves = list(game.valid_moves(to_move))

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def uct_value(self, child, K):
        if child.visits == 0:
            return float("inf")
        exploitation = child.wins / child.visits
        exploration = np.sqrt(K * np.log(self.visits) / child.visits)
        return exploitation + exploration

    def best_child(self, K=1.4):
        best_score = -float("inf")
        best_move, best_child = None, None
        for mv, ch in self.children.items():
            score = self.uct_value(ch, K)
            if score > best_score:
                best_score = score
                best_move, best_child = mv, ch
        return best_move, best_child


class AgentMCTS:
    

    def __init__(self, board: BitboardReversi, nb_simu=300, K=1.4):
        self.board = board
        self.nb_simu = nb_simu
        self.K = K

    def play(self, to_move):
        start_time = time.time()
        root = MCTSNode(self.board.copy(), to_move)
        if not root.untried_moves:
            return (-1, -1)

        while time.time() - start_time < 1.9:  # ≤ 2s par coup
            node = root
            game_copy = node.game.copy()
            cur_player = node.to_move

           
            while node.is_fully_expanded() and node.children and not game_copy.game_over():
                mv, node = node.best_child(self.K)
                game_copy.make_move(mv[0], mv[1], cur_player)
                cur_player = -cur_player

            
            if node.untried_moves and not game_copy.game_over():
                mv = random.choice(node.untried_moves)
                node.untried_moves.remove(mv)
                game_copy.make_move(mv[0], mv[1], cur_player)
                child = MCTSNode(game_copy.copy(), -cur_player, parent=node, move_from_parent=mv)
                node.children[mv] = child
                node = child
                cur_player = -cur_player

            winner = rollout(game_copy, cur_player)

            
            while node:
                node.visits += 1
                if winner == -node.to_move:  
                    node.wins += 1
                node = node.parent

      
        best_move = max(root.children.items(), key=lambda kv: kv[1].visits)[0]
        return best_move



Agent = AgentMCTS
