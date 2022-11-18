from random import choice
from module_other.coordinates_module import FIELD_DICT

def smarter_moves(enemy_dir, gx, gy, field):
    order_candi = [0, 1, 2, 3]
    order_0th_candi = []
    order_2nd_candi = []
    order_3rd_candi = []
    dx = (1, 0, -1, 0)
    dy = (0, -1, 0, 1)
    corner = [(0,0), (14,0), (0,8), (14,8)]
    order_candi.remove((enemy_dir + 2) % 4)

    condition0 = FIELD_DICT['player'] + FIELD_DICT['apple']
    condition2 = FIELD_DICT['bomb']
    condition3 = FIELD_DICT['enemy'] + FIELD_DICT['skin'] + FIELD_DICT['box']

    if(gx == 14 and 0 in order_candi):
        order_candi.remove(0)
    elif(gx == 0 and 2 in order_candi):
        order_candi.remove(2)
    if(gy == 0 and 1 in order_candi):
        order_candi.remove(1)
    elif(gy == 8 and 3 in order_candi):
        order_candi.remove(3)

    for mov in order_candi:
        predict = field[gx+1+dx[mov]][gy+1+dy[mov]]
        if(predict & condition0):
            order_0th_candi.append(mov)

    for items in order_0th_candi:
        order_candi.remove(items)
    
    for mov in order_candi:
        predict = field[gx+1+dx[mov]][gy+1+dy[mov]]
        if((predict & condition2) or ((gx+dx[mov], gy+dy[mov]) in corner)):
            order_2nd_candi.append(mov)

    for items in order_2nd_candi:
        order_candi.remove(items)

    for mov in order_candi:
        predict = field[gx+1+dx[mov]][gy+1+dy[mov]]
        if(predict & condition3):
            order_3rd_candi.append(mov)

    for items in order_3rd_candi:
        order_candi.remove(items)
    
    for candi in (order_0th_candi, order_candi, order_2nd_candi, order_3rd_candi):
        if(len(candi) > 0):
            return choice(candi)