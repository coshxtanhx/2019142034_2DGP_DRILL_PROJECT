def circle_move(gx, gy, enemy_dir):
    order = enemy_dir
    if(gx <= 1 and gy <= 1):
        order = 3
    elif(gx <= 1 and gy >= 7):
        order = 0
    elif(gx >= 13 and gy <= 1):
        order = 2
    elif(gx >= 13 and gy >= 7):
        order = 1

    return order