from coordinates_module import FIELD_DICT

dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

def is_possible(order, enemy_dir, gx, gy, field):
    if((enemy_dir + 2) % 4 == order):
        return -1
    predict = field[gx + 1 + dx[order]][gy + 1 + dy[order]]
    obj_to_avoid = FIELD_DICT['wall'] + FIELD_DICT['enemy']
    if(predict & obj_to_avoid):
        return -1
    return order