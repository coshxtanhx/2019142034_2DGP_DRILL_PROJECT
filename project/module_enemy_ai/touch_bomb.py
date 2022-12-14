from module_enemy_ai.just_go import come_here
from module_enemy_ai.cannot_go import is_possible
from collections import deque
from module_other.term_table import *
import module_other.server as sv

last_bomb_gx, last_bomb_gy = 0, 0
dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

def bomb_finding_move(enemy_dir, gx, gy, field):
    bombs = sv.bomb
    if(not(bombs)): return -1
    last_enemy_bomb = -1
    for idx in range(len(bombs)-1, -1, -1):
        if(bombs[idx].owner == ENEMY_OWNS):
            last_enemy_bomb = idx
            break
    else: return -1
    last_bomb_gx, last_bomb_gy = \
        bombs[last_enemy_bomb].gx, bombs[last_enemy_bomb].gy
    order = come_here(enemy_dir, gx, gy, last_bomb_gx, last_bomb_gy, 0)

    order = is_possible(order, enemy_dir, gx, gy, field)

    return order