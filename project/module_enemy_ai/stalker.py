from module_enemy_ai.just_go import come_here
from module_enemy_ai.cannot_go import is_possible
from module_other.coordinates_module import *

dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

def stalking_move(enemy_dir, gx, gy, field):
    import module_object.snake_player as sp
    ox, oy = coordinates_to_grid(sp.Blue_body.hx, sp.Blue_body.hy)

    order = come_here(enemy_dir, gx, gy, ox+1, oy+1, 4)

    order = is_possible(order, enemy_dir, gx, gy, field)

    return order