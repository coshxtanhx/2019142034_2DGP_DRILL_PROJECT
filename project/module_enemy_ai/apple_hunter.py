from module_enemy_ai.just_go import come_here
from module_enemy_ai.cannot_go import is_possible

apple_gx, apple_gy = 0, 0
dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

def apple_finding_move(enemy_dir, gx, gy, field, option=0):    
    order = come_here(enemy_dir, gx, gy, apple_gx, apple_gy, option)

    order = is_possible(order, enemy_dir, gx, gy, field)

    return order