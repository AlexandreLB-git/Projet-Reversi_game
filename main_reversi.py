from bitreversi import BitboardReversi
import os
import sys
import importlib.util
import multiprocessing as mp
import itertools
import copy
from collections import defaultdict
import logging
os.makedirs("logs", exist_ok=True)

# Nom du fichier de log
log_file = os.path.join("logs", "tournament.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'),  # fichier
        logging.StreamHandler()  # console
    ]
)
logger = logging.getLogger(__name__)
AGENTS_DIR = "agents"
NUM_MATCHES_EACH_SIDE = 5
TIME_PER_MOVE = 2

GAME = BitboardReversi()

def load_agent(agent_dir):
    agent_path = os.path.join(AGENTS_DIR, agent_dir)
    agent_file = os.path.join(agent_path, "agent.py")

    # Ajouter le répertoire de l'agent dans sys.path pour pouvoir importer ses sous-modules
    sys.path.insert(0, agent_path)

    try:
        spec = importlib.util.spec_from_file_location(agent_dir, agent_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        # Retirer le chemin pour éviter les conflits avec d'autres agents
        sys.path.pop(0)

    # Chercher la première classe qui commence par "Agent"
    for attr in dir(module):
        if attr.startswith("Agent"):
            return  getattr(module, attr)

    raise ValueError(f"Aucune classe d'agent trouvée dans {agent_file}")
    

def run_agent_move(agent, board, player, result_queue):
    """Code exécuté dans un processus séparé pour respecter le timeout."""
    try:
        move = agent.play(player)
        result_queue.put(move)
    except Exception as e:
        logger.error(e)
        result_queue.put(None)

def play_game(agent1_class, agent2_class,  time_limit=1.0):
    GAME.reset()
    board_init = GAME
    agents = {
        1: agent1_class(board_init.copy()),
        -1: agent2_class(board_init.copy()),
    }
    board = board_init.copy()
    player = 1

    while not board.game_over():
        agent = agents[player]
        agent.board = board.copy()

        legal_moves = board.valid_moves(player)
        if not legal_moves:
            player = -player
            continue

        result_queue = mp.Queue()
        p = mp.Process(target=run_agent_move, args=(agent, board, player, result_queue))
        p.start()
        p.join(timeout=time_limit)

        if p.is_alive():
            p.terminate()
            p.join()
            logger.error(f"Too late for player {1 if player>0 else -1}")
            move = None
        else:
            move = result_queue.get()

        if move not in legal_moves:
            logger.error(f"Illegal move for player {1 if player>0 else -1}")
            move = None

        if move is not None:
            board.make_move(*move, player)
        else:
            return -player*100

        player = -player

    return board.score()

# --- Tournoi Round-Robin ---
def run_tournament():
    agent_dirs = sorted(os.listdir(AGENTS_DIR))
    agents = {name: load_agent(name) for name in agent_dirs}
    scores = defaultdict(int)
    results = defaultdict(lambda: {"wins": 0, "draws": 0, "losses": 0})
    history = defaultdict(list)
    agent_names = list(agents.keys())
    pairs = list(itertools.combinations(agent_names, 2))
    for a1, a2 in pairs:
        for i in range(NUM_MATCHES_EACH_SIDE):
            # Aller : A1 (noir), A2 (blanc)
            logger.debug(f"Playing : {a1} vs {a2} match {i}")
            winner = play_game(agents[a1], agents[a2],TIME_PER_MOVE)
            if winner >0:
                scores[a1] += 1
                results[a1]["wins"] += 1
                results[a2]["losses"] += 1
            elif winner <0:
                scores[a2] += 1
                results[a2]["wins"] += 1
                results[a1]["losses"] += 1
            else:
                scores[a1] += 0.5
                scores[a2] += 0.5
                results[a1]["draws"] += 1
                results[a2]["draws"] += 1
            history[a1].append((a1,a2,winner))
            history[a2].append((a1,a2,winner))
            # Retour : A2 (noir), A1 (blanc)
            winner = play_game(agents[a2], agents[a1], TIME_PER_MOVE)
            if winner >0 :
                scores[a2] += 1
                results[a2]["wins"] += 1
                results[a1]["losses"] += 1
            elif winner <0:
                scores[a1] += 1
                results[a1]["wins"] += 1
                results[a2]["losses"] += 1
            else:
                scores[a1] += 0.5
                scores[a2] += 0.5
                results[a1]["draws"] += 1
                results[a2]["draws"] += 1
            history[a1].append((a2,a1,winner))
            history[a2].append((a2,a1,winner))

    logger.info("\n=== Results ===")
    sorted_agents = sorted(agent_dirs, key=lambda name: scores[name], reverse=True)
    for name in sorted_agents:
        s = scores[name]
        r = results[name]
        print(f"{name:20} | Score: {s:4.1f} | W: {r['wins']} D: {r['draws']} L: {r['losses']}")
    logger.info("\n*** History \n***")
    for name in sorted_agents:
        print(f"{name} : " + "|".join(f"{m1} vs {m2} : {score}" for (m1,m2,score) in history[name]))
if __name__ == "__main__":
    run_tournament()