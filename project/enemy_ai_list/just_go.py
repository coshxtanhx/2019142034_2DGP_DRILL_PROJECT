from random import choice
from coordinates_module import get_distance

def aim_arrived(gx, gy, aim_gx, aim_gy, option):
    if get_distance(gx, gy, aim_gx, aim_gy) <= option:
        return True
    else:
        return False

def come_here(enemy_dir, gx, gy, aim_gx, aim_gy, option = 1.5):
    order = enemy_dir
    order_pack = [enemy_dir, enemy_dir]

    if(aim_gx > gx):
        order_pack[0] = 0
    elif(aim_gx < gx):
        order_pack[0] = 2
    else:
        order_pack[0] = None

    if(aim_gy > gy):
        order_pack[1] = 3
    elif(aim_gy < gy):
        order_pack[1] = 1
    else:
        order_pack[1] = None

    if(aim_arrived(gx, gy, aim_gx, aim_gy, option)):
        return -1

    elif(order_pack[0] == None):
        order = order_pack[1]
    elif(order_pack[1] == None):
        order = order_pack[0]
    else:
        order = choice(order_pack)

    return order