from coordinates_module import FIELD_DICT

order_flag = True #T: vert / F: hori

dx = (1, 0, -1, 0)
dy = (0, -1, 0, 1)

def vert_sweeps(gx, gy):
    global order_flag
    if(gx == 14 and gy == 0):
        order_flag = False
        order = hori_sweeps(gx, gy)
    elif(gx % 2 == 0 and gy == 0):
        order = 0
    elif(gx % 2 == 0):
        order = 1
    elif(gx % 2 == 1 and gy == 8):
        order = 0
    elif(gx % 2 == 1):
        order = 3
    return order

def hori_sweeps(gx, gy):
    global order_flag
    if(gy == 8 and gx == 0):
        order_flag = True
        order = vert_sweeps(gx, gy)
    elif(gy % 2 == 0 and gx == 0):
        order = 3
    elif(gy % 2 == 0):
        order = 2
    elif(gy % 2 == 1 and gx == 14):
        order = 3
    elif(gy % 2 == 1):
        order = 0
    return order

def sweep_move(enemy_dir, gx, gy, field):
    global order_flag
    order = enemy_dir
    if(order_flag):
        order = vert_sweeps(gx, gy)
    else:
        order = hori_sweeps(gx, gy)

    if((enemy_dir + 2) % 4 == order):
        return -1
    predict = field[gx + 1 + dx[order]][gy + 1 + dy[order]]
    obj_to_avoid = FIELD_DICT['wall'] + FIELD_DICT['enemy']
    if(predict & obj_to_avoid):
        return -1

    return order