from coordinates_module import *
from pico2d import *
from collections import deque

def bomb_draw_case(option, is_enemy, cnt, frame, x, y):
    if(option == 0):
        bomb.image[cnt-1+is_enemy].clip_draw(60 * (frame % 3), 0, 60, 60, x, y)
    elif(option == 1):
        bomb.image2.clip_draw(60 * (frame % 3), 60 * (cnt-1), 60, 60, x, y)
    elif(option == 2):
        bomb.image3.clip_draw(60 * (frame % 3), 60 * (cnt-1), 60, 60, x, y)
    elif(option == 3):
        bomb.image4.clip_draw(60 * (frame % 3), 60 * (cnt-1), 60, 60, x, y)

class Ice():
    image = None
    def __init__(self, gx, gy):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.frame = 700
        if(Ice.image == None):
            Ice.image = load_image('img/ice.png')
    def draw(self, field_array):
        field_array[self.gx][self.gy] |= FIELD_DICT['ice']
        drawframe = (701 - self.frame) if (self.frame > 694) else 6
        drawframe = (self.frame + 1) if (self.frame < 5) else drawframe
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, \
            10 * drawframe, 10 * drawframe)


class explosion():
    image = None
    def __init__(self, gx, gy, damage):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.frame = 6
        self.damage = damage
        if(explosion.image == None):
            explosion.image = load_image('img/explode.png')
    def draw(self):
        self.image.clip_draw(60 * (self.frame // 2), 0, 60, 60, self.x, self.y)

class bomb():
    image = None
    image2 = None
    image3 = None
    image4 = None
    def __init__(self, x, y, damage, option = 0):
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        self.counter = 350
        self.damage = damage
        self.option = option
        self.is_enemy = 5 if (self.damage == 0) else 0
        if bomb.image == None:
            bomb.image = \
                [load_image('img/bomb_' + str(i) + '.png') for i in range(1, 11)]
            bomb.image2 = load_image('img/bomb_cross.png')
            bomb.image3 = load_image('img/bomb_ice.png')
            bomb.image4 = load_image('img/bomb_ice_cross.png')
    def explode(self, field_array, explodes):
        for x in range(self.gx+1, 0, -1):
            field_array[x][self.gy+1] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(x, self.gy+1, self.damage))
        for x in range(self.gx+1, 16, +1):
            field_array[x][self.gy+1] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(x, self.gy+1, self.damage))
        for y in range(self.gy+1, 10, +1):
            field_array[self.gx+1][y] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(self.gx+1, y, self.damage))
        for y in range(self.gy+1, 0, -1):
            field_array[self.gx+1][y] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(self.gx+1, y, self.damage))
        self.x = -65535
    def explode_cross(self, field_array, explodes):
        for i in range(0, 9, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy+i < 9): break
            field_array[self.gx+i+1][self.gy+i+1] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(self.gx+i+1, self.gy+i+1, self.damage))
        for i in range(1, 9, 1):
            if not(-1 < self.gx-i < 15 and -1 < self.gy+i < 9): break
            field_array[self.gx-i+1][self.gy+i+1] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(self.gx-i+1, self.gy+i+1, self.damage))
        for i in range(1, 9, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy-i < 9): break
            field_array[self.gx+i+1][self.gy-i+1] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(self.gx+i+1, self.gy-i+1, self.damage))
        for i in range(1, 9, 1):
            if not(-1 < self.gx-i < 15 and -1 < self.gy-i < 9): break
            field_array[self.gx-i+1][self.gy-i+1] |= FIELD_DICT['explode']
            explodes.appendleft(explosion(self.gx-i+1, self.gy-i+1, self.damage))
        self.x = -65535
    def explode_ice(self, field_array, ices):
        ice_removing_obj = FIELD_DICT['enemy'] + FIELD_DICT['explode'] \
            + FIELD_DICT['bomb'] + FIELD_DICT['apple'] + FIELD_DICT['ice']
        for x in range(-3, 4, 1):
            if not(-1 < self.gx+x < 15): continue
            if field_array[self.gx+x+1][self.gy+1] & ice_removing_obj: continue
            ices.append(Ice(self.gx+x+1, self.gy+1))
        for y in range(-3, 4, 1):
            if not(-1 < self.gy+y < 9): continue
            if field_array[self.gx+1][self.gy+y+1] & ice_removing_obj: continue
            ices.append(Ice(self.gx+1, self.gy+1+y))
    def explode_ice_cross(self, field_array, ices):
        ice_removing_obj = FIELD_DICT['enemy'] + FIELD_DICT['explode'] \
            + FIELD_DICT['bomb'] + FIELD_DICT['apple'] + FIELD_DICT['ice']
        for i in range(-2, 3, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy+i < 9): continue
            if field_array[self.gx+i+1][self.gy+i+1] & ice_removing_obj: continue
            ices.append(Ice(self.gx+1+i, self.gy+1+i))
        for i in range(-2, 3, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy-i < 9): continue
            if field_array[self.gx+i+1][self.gy-i+1] & ice_removing_obj: continue
            ices.append(Ice(self.gx+1+i, self.gy+1-i))
    def draw(self, field_array, explodes, ices, frame):
        cnt = ceil(self.counter / 70)
        if(self.counter > 0):
            bomb_draw_case(self.option, self.is_enemy, cnt, frame, self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['bomb']
        elif(self.counter == 0 or self.counter <= -65535):
            if(self.option == 0):
                self.explode(field_array, explodes)
            elif(self.option == 1):
                self.explode_cross(field_array, explodes)
            elif(self.option == 2):
                self.explode_ice(field_array, ices)
            elif(self.option == 3):
                self.explode_ice_cross(field_array, ices)
        else:
            return