from enemy_ai_list.just_go import come_here
from enemy_ai_list.cannot_go import is_possible

aim_points = [(1,1), (1,7), (13, 7), (13, 1)]
aim_flag = 2

def circle_move(enemy_dir, gx, gy, field):
    global aim_flag
    order = enemy_dir

    order = come_here(enemy_dir, gx, gy, *(aim_points[aim_flag]))

    if(order == -1):
        aim_flag = (aim_flag + 1) % 4

    order = is_possible(order, enemy_dir, gx, gy, field)

    return order