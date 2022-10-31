from coordinates_module import *
from collections import deque
from pico2d import *

img_snake_orange_head = \
    [load_image('img/snake_orange_head_' + str(i) + '.png') for i in range(4)]
img_snake_orange_body = load_image('img/snake_orange_body.png')

img_snake_green_head = \
    [load_image('img/snake_green_head_' + str(i) + '.png') for i in range(4)]
img_snake_green_body = load_image('img/snake_green_body.png')

img_snake_purple_head = \
    [load_image('img/snake_purple_head_' + str(i) + '.png') for i in range(4)]
img_snake_purple_body = load_image('img/snake_purple_body.png')

img_snake_brown_head = \
    [load_image('img/snake_brown_head_' + str(i) + '.png') for i in range(4)]
img_snake_brown_body = load_image('img/snake_brown_body.png')

class Enemy_body():
    enemy_direction = 0
    enemy_order = 0
    def __init__(self, number, color = 'orange', x=40, y=-1):
        if(y == -1):
            self.x, self.y = grid_to_coordinates(0, 8)
        else:
            self.x, self.y = x, y
        self.frame = 0
        self.number = number
        self.image = 0
        self.color = color
    def moves(self, enemy_char, field_array):
        if(self.number == len(enemy_char) - 1):
            self.x, self.y = enemy_char[0].x + dx[Enemy_body.enemy_direction], \
                enemy_char[0].y + dy[Enemy_body.enemy_direction]
            self.number = 0
            enemy_char.rotate(1)
        else:
            if(self.number == 0):
                if(self.x % 60 == 40 and self.y % 60 == 40):
                    Enemy_body.enemy_direction = Enemy_body.enemy_order
            self.number += 1
        gx, gy = coordinates_to_grid(self.x, self.y)
        field_array[gx+1][gy+1] |= FIELD_DICT['enemy']

    def draw(self):
        if(self.number == 0):
            self.image = \
                (eval('img_snake_' + self.color + \
                    '_head'))[Enemy_body.enemy_direction]
        else:
            self.image = eval('img_snake_' + self.color + '_body')
        self.image.draw(self.x, self.y)