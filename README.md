# Reversi AI Tournament
Description

This project is a Python-based Reversi (Othello) game simulator, featuring multiple intelligent agents that compete in an automated tournament. The project includes:

A classic bitboard implementation (BitboardReversi) for optimized performance.

A numpy-based board version for educational and pedagogical purposes.

Agents implementing different strategies:
-Random Agent
-Monte Carlo Tree Search (MCTS), including FlatMCTS and real-time MCTS with exploration/exploitation strategies
-Multi-armed bandit and greedy strategies

A Round-Robin tournament to measure and compare agent performance.

Per-move time management and exception handling to prevent timeouts.

Detailed logging of games in logs/tournament.log.

## Project Structure
```
.
├── agents/             # Folder containing the agents competing in the tournament
├── logs/               # Tournament logs
├── README              # readme english version
├── README_FR           # readme french version
├── bitreversi.py      # Bitboard-based Reversi implementation
├── main_reversi.py     # Tournament launcher
├── reversi.py          # Numpy-based Reversi implementation
├── tme1.ipynb          # Notebook with instructions and tests for tme1
├── tme1.py             # Initial experiments with random agents
├── tme2.py             # Simulation and Monte Carlo functions
├── tme2.ipynb          # Notebook with instructions and tests for tme2
├── tme3.py             # FlatMCTS and MCTS agents
├── tme3.ipynb          # Notebook with instructions and tests for tme3
├── tme4.py             # Tournament between agents and benchmarking
└── tme4.ipynb          # Notebook with instructions and tests for tme4
```


### Notes on Agents
- **AgentRandom**: Chooses moves entirely at random, used as a baseline for testing.  
- **Agent_21310941_21311189**: Custom agent using Monte Carlo Tree Search (MCTS) and statistical decision-making strategies. Performs simulations to select moves with the best estimated win ratio.



### Update — Tournament Score Files Added (08/12/2025)

Two new files have been added to the repository to provide a complete record of the Reversi AI tournament organized in class:

tournament_Groupe_5.txt — results of the group stage

tournament_FINAL.txt — results of the final tournament including all participating student bots

These files contain:

full rankings (wins, draws, losses, and total scores)

detailed match results for every round and every agent

score differentials and color assignments (a1_black / a2_black)

They document the entire competitive process from the qualification phase to the final ranking.

### Tournament Summary

Our agent Agent_21310941_21311189 finished 1st in Group 5 and 1st in the overall final ranking, making it the top-performing agent among all bots coded by the students.
