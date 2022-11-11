from coordinates_module import *
from collections import deque
from pico2d import *
from enemy_movement_ai import enemy_ai

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

img_armor = load_image('img/armor.png')

COLOR_DICT = {'1': 'orange', '2': 'brown', '3': 'purple', '4': 'green'}
COLOR_DICT2 = {'orange': 1, 'brown': 2, 'purple': 3, 'green': 4}

AI_DICT = {
    (3, 1): 1, (2, 1): 2, (1, 1): 0, (0, 1): 3,
    (3, 2): 1, (2, 2): 2, (1, 2): 0, (0, 2): 3,
    (3, 3): 1, (2, 3): 2, (1, 3): 0, (0, 3): 3,
    (3, 4): 1, (2, 4): 2, (1, 4): 0, (0, 4): 3,
}

class Enemy_body():
    enemy_direction = 0
    enemy_order = 0
    bomb_cool_down = 500
    enemy_hp = 960
    armored = []
    color = None
    ai = 0
    def __init__(self, number, color = 'orange', x=40, y=-1):
        if(y == -1):
            self.x, self.y = grid_to_coordinates(0, 8)
        else:
            self.x, self.y = x, y
        self.gx, self.gy = coordinates_to_grid(self.x, self.y)
        self.frame = 0
        self.number = number
        self.image = 0
        Enemy_body.color = color
        self.armored = False
    def moves(self, enemy_char, field_array):
        if(self.number == len(enemy_char) - 1):
            self.x, self.y = enemy_char[0].x + dx[Enemy_body.enemy_direction], \
                enemy_char[0].y + dy[Enemy_body.enemy_direction]
            self.number = 0
            enemy_char.rotate(1)
        else:
            self.number += 1            

    def draw(self, field_array):
        if(self.number == 0):
            self.image = \
                (eval('img_snake_' + Enemy_body.color + \
                    '_head'))[Enemy_body.enemy_direction]
        else:
            self.image = eval('img_snake_' + Enemy_body.color + '_body')
        self.image.draw(self.x, self.y)
        field_array[self.gx+1][self.gy+1] |= FIELD_DICT['enemy']
        if(self.number-4 in Enemy_body.armored or \
            self.number-2 in Enemy_body.armored or \
            self.number+0 in Enemy_body.armored or \
            self.number+2 in Enemy_body.armored or \
            self.number+4 in Enemy_body.armored):
            img_armor.draw(self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['armor']
    
    def enemy_ai_update(enemy_head, field_array):
        Enemy_body.change_ai()
        if(enemy_head.x % 60 == 40 and enemy_head.y % 60 == 40):
            Enemy_body.enemy_direction = enemy_ai(Enemy_body.enemy_direction, \
                *coordinates_to_grid(enemy_head.x, enemy_head.y), \
                field_array, Enemy_body.ai)

    def reset():
        Enemy_body.enemy_direction = 0
        Enemy_body.enemy_order = 0
        Enemy_body.bomb_cool_down = 500
        Enemy_body.enemy_hp = 960 // 96
        Enemy_body.armored = []
        Enemy_body.ai = 0

    def change_ai():
        Enemy_body.ai = \
            AI_DICT[(Enemy_body.enemy_hp // 241, COLOR_DICT2[Enemy_body.color])]