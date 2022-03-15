import sys
import time
import random
import copy

import numpy as np
from player import Player

from chess_utils import ChessEnvV2, ChessOutcomes


def ch_ender_grids(env, prev_board, message, move=None):
    print(f'\n\n============{message}=============')
    grid = env.board_to_grid(prev_board)
    env.render_grid(grid)

    if move != None:
        env.render_moves([env.action_to_move(move)], mode="human")

    env.render()
    print(f"======================================\n\n")



def ch_play_chess_game(white: Player, black: Player, chess_env: ChessEnvV2) -> ChessOutcomes:

    state = chess_env.reset()
    white.p_get_ready_to_play()
    black.p_get_ready_to_play()
    done = False

    while True:

        ################################# white move #################################
        if len(chess_env.possible_actions) == 0:
            print(f'No possible moves. done: {done}')
            break
        move = white.p_make_move(state, chess_env.possible_actions)

        # perform action
        try:
            state, reward, done, _ = chess_env.step(move)
        except:
            white.p_game_over(ChessOutcomes.bad_exit)
            black.p_game_over(ChessOutcomes.bad_exit)
            return ChessOutcomes.bad_exit

        white.p_recieve_reward(reward)
        if done:
            break


        ################################# black move #################################
        if len(chess_env.possible_actions) == 0:
            print(f'No possible moves. done: {done}')
            break
        move = black.p_make_move(state, chess_env.possible_actions)

        # perform action
        try:
            state, reward, done, _ = chess_env.step(move)
        except:
            white.p_game_over(ChessOutcomes.bad_exit)
            black.p_game_over(ChessOutcomes.bad_exit)
            return ChessOutcomes.bad_exit
            

        black.p_recieve_reward(reward)
        if done:
            break

    if chess_env.white_king_is_checked and len(chess_env.possible_actions) == 0:
        white.p_game_over(ChessOutcomes.black_win)
        black.p_game_over(ChessOutcomes.black_win)
        return ChessOutcomes.black_win
    elif chess_env.black_king_is_checked and len(chess_env.possible_actions) == 0:
        white.p_game_over(ChessOutcomes.white_win)
        black.p_game_over(ChessOutcomes.white_win)
        return ChessOutcomes.white_win
    else:
        white.p_game_over(ChessOutcomes.draw)
        black.p_game_over(ChessOutcomes.draw)
        return ChessOutcomes.draw

def main():

    # Play against self (no oppenent)
    env = ChessEnvV2(opponent='none', log=False)
    white = Player()
    black = Player()

    num_episodes = 100
    for i in range(num_episodes):

        outcome = ch_play_chess_game(white, black, env)
        
        if not outcome is ChessOutcomes.bad_exit:
            print(">" * 5, "GAME", i, f"REWARD: {white.p_get_last_reward() + black.p_get_last_reward()}\n")
            # print(f'TOTAL MOVES: {env.move_count}')
            # print(f'Number of moves with no captures or pawn moves: {env.no_captures_or_pawn_moves}')
            # if env.white_king_is_checked and len(env.possible_actions) == 0:
            #     print(f'Black wins')
            # elif env.black_king_is_checked and len(env.possible_actions) == 0:
            #     print(f'White wins')
            # else:
            #     print('Draw')
            # print('')

        else: 
            # if this happens, it means something in the 
            # chess engine messed up and so the game should
            # be rejected and the environment restarted
            print('=========== Game exited with an error. Do not update players ===========\n')
	


if __name__ == '__main__':
    main()