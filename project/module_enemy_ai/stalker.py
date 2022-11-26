from module_enemy_ai.just_go import come_here
from module_enemy_ai.cannot_go import is_possible
from module_other.coordinates_module import *
import module_other.server as sv

dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

def stalking_move(enemy_dir, gx, gy, field):
    ox, oy = coordinates_to_grid(sv.player_head.x, sv.player_head.y)

    order = come_here(enemy_dir, gx, gy, ox+1, oy+1, 4)

    order = is_possible(order, enemy_dir, gx, gy, field)

    return order