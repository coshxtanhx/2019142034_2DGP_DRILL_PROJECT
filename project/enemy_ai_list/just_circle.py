from coordinates_module import FIELD_DICT, get_distance
from enemy_ai_list.just_go import come_here

dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

aim_points = [(1,1), (1,7), (13, 7), (13, 1)]
aim_flag = 2

def circle_move(enemy_dir, gx, gy, field):
    global aim_flag
    order = enemy_dir

    order = come_here(enemy_dir, gx, gy, *(aim_points[aim_flag]))

    if(order == -1):
        aim_flag = (aim_flag + 1) % 4

    if((enemy_dir + 2) % 4 == order):
        return -1
    predict = field[gx + 1 + dx[order]][gy + 1 + dy[order]]
    obj_to_avoid = FIELD_DICT['wall'] + FIELD_DICT['enemy']
    if(predict & obj_to_avoid):
        return -1

    return order