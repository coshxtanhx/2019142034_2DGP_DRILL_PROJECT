from coordinates_module import *
from pico2d import *
from collections import deque

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
        self.image.clip_draw(0 + 60 * (self.frame // 2), 0, 60, 60, self.x, self.y)

class bomb():
    image = None
    def __init__(self, x, y, damage):
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        self.counter = 350
        self.damage = damage
        self.is_enemy = 5 if (self.damage == 0) else 0
        if bomb.image == None:
            bomb.image = \
                [load_image('img/bomb_' + str(i) + '.png') for i in range(1, 11)]
    def explode(self, field_array, explodes):
        for x in range(self.gx+1, 0, -1):
            field_array[x][self.gy+1] |= 64
            explodes.appendleft(explosion(x, self.gy+1, self.damage))
        for x in range(self.gx+1, 16, +1):
            field_array[x][self.gy+1] |= 64
            explodes.appendleft(explosion(x, self.gy+1, self.damage))
        for y in range(self.gy+1, 10, +1):
            field_array[self.gx+1][y] |= 64
            explodes.appendleft(explosion(self.gx+1, y, self.damage))
        for y in range(self.gy+1, 0, -1):
            field_array[self.gx+1][y] |= 64
            explodes.appendleft(explosion(self.gx+1, y, self.damage))
        self.x = -65535
    def draw(self, field_array, explodes, frame):
        cnt = ceil(self.counter / 70)
        if(self.counter > 0):
            self.image[cnt-1+self.is_enemy].clip_draw(0 + 60 * (frame % 3), 0, \
                60, 60, self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['bomb']
        elif(self.counter == 0 or self.counter <= -65535):
            self.explode(field_array, explodes)
        else:
            return