import gym
import gym_chess

from gym_chess import ChessEnvV2
from enum import Enum

ChessOutcomes = Enum('ChessOutcomes', 'white_win black_win draw bad_exit')