from module_enemy_ai.cannot_go import is_possible

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

    order = is_possible(order, enemy_dir, gx, gy, field)

    return order