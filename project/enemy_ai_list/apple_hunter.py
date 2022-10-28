from coordinates_module import FIELD_DICT
from enemy_ai_list.just_go import come_here

apple_gx, apple_gy = 0, 0
dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

def apple_finding_move(enemy_dir, gx, gy, field):    
    order = come_here(enemy_dir, gx, gy, apple_gx, apple_gy, 0)

    if((enemy_dir + 2) % 4 == order):
        return -1
    predict = field[gx + 1 + dx[order]][gy + 1 + dy[order]]
    obj_to_avoid = FIELD_DICT['wall'] + FIELD_DICT['enemy']
    if(predict & obj_to_avoid):
        return -1

    return order