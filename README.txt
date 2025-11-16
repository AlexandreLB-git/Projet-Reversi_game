#Projet-Reversi_game

Reversi AI Tournament
Description

This project is a Reversi (Othello) game simulator in Python, with multiple implementations of intelligent agents capable of competing in an automated tournament. The project includes:

A classic implementation of the game using a bitboard (BitboardReversi) for optimized performance.

A version with a numpy-based board for more pedagogical manipulation.

Agents playing with different strategies:

Random Agent

Monte Carlo Tree Search (MCTS), including FlatMCTS and real-time MCTS with exploration/exploitation

Multi-armed bandit and greedy strategies

A Round-Robin tournament to measure and compare agent performance.

Per-move time management and exception handling to prevent timeouts.

Detailed logging of games in logs/tournament.log.

Project Structure
.
├── agents/             # Folder containing agents competing in the tournament
├── logs/               # Tournament logs
├── reversi.py          # Reversi game implementation (bitboard and numpy)
├── tme1.py             # Initial experiments with random agents
├── tme2.py             # Simulation and Monte Carlo functions
├── tme3.py             # FlatMCTS and MCTS agents
├── tme4.py             # Tournament between agents and benchmarking
├── main.py             # Tournament launcher
├── tme1.ipynb          # Notebook with instructions and tests for tme1
├── tme2.ipynb          # Notebook with instructions and tests for tme2
├── tme3.ipynb          # Notebook with instructions and tests for tme3
└── tme4.ipynb          # Notebook with instructions and tests for tme4
