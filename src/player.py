import random
from typing import Any, Dict, List
from numbers import Number
from chess_utils import ChessOutcomes

class Player:
    def __init__(self):
        self.games_played = 0
        self.recieved_rewards = list()
        self.total_rewards = 0

    def p_make_move(self, state: Dict[Any, Any], legal_moves: List[Any]):
        move = random.choice(legal_moves)
        return move

    def p_recieve_reward(self, reward: Number):
        self.recieved_rewards[self.games_played] += reward
        self.total_rewards += reward

    def p_get_ready_to_play(self):
        self.recieved_rewards.append( 0 )

    def p_game_over(self, outcome: ChessOutcomes):

        if outcome is ChessOutcomes.bad_exit:
            self.recieved_rewards[-1] = 0

        self.games_played += 1

    def p_get_last_reward(self):
        return self.recieved_rewards[-1]
