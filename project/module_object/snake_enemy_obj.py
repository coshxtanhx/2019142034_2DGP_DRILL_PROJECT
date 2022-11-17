from module_other.coordinates_module import *
from collections import deque
from pico2d import *
from random import choice
from module_object.bomb_obj import bomb
from module_enemy_ai.enemy_movement_ai import enemy_ai
import module_other.game_world as gw
import module_other.state_changer as sc

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
    (3, 3): 1, (2, 3): 0, (1, 3): 1, (0, 3): 3,
    (3, 4): 0, (2, 4): 3, (1, 4): 4, (0, 4): 5,
}

bomb_type_list = (
    (0,), (0,1), (0, 0,1,3), (0,0, 1,3,2,2), (3, 3, 3, 2, 2, 2, 1, 0)
)

class Enemy_body():
    enemy_direction = 0
    enemy_order = 0
    bomb_cool_down = 500
    enemy_hp = 960
    armored = []
    color = None
    ai = 0
    bomb_type = 0
    length = 12*(6-1)+1
    hx, hy = grid_to_coordinates(0, 8)
    tx, ty = hx, hy
    damaged = 0
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
    def get_damaged(damage):
        if Enemy_body.damaged < damage:
            Enemy_body.damaged = damage
    def update(self):
        if(self.number == self.length - 1):
            self.x, self.y = Enemy_body.hx + dx[Enemy_body.enemy_direction], \
                Enemy_body.hy + dy[Enemy_body.enemy_direction]
            self.number = 0
            if Enemy_body.bomb_cool_down > 0: Enemy_body.bomb_cool_down -= 1
            if Enemy_body.damaged:
                Enemy_body.enemy_hp -= Enemy_body.damaged
                Enemy_body.damaged = 0
        else:
            if(self.number == 0):
                self.enemy_ai_update()
            self.number += 1
        if Enemy_body.enemy_hp <= 0:
            Enemy_body.enemy_hp = 0
            import module_state.snake_move as sm
            sm.isended = 1

    def draw(self):
        self.gx, self.gy = coordinates_to_grid(self.x, self.y)
        if(self.number == 0):
            gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['ehead']
            Enemy_body.hx, Enemy_body.hy = self.x, self.y
            return
        else:
            self.image = eval('img_snake_' + Enemy_body.color + '_body')
            if(self.number == self.length-1):
                Enemy_body.tx, Enemy_body.ty = self.x, self.y
        self.image.draw(self.x, self.y)
        if(self.number == self.length - 1):
            (eval('img_snake_' + Enemy_body.color + '_head'))\
                [Enemy_body.enemy_direction].draw(Enemy_body.hx, Enemy_body.hy)
        gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['enemy']

        if(self.number-4 in Enemy_body.armored or \
            self.number-2 in Enemy_body.armored or \
            self.number+0 in Enemy_body.armored or \
            self.number+2 in Enemy_body.armored or \
            self.number+4 in Enemy_body.armored):
            img_armor.draw(self.x, self.y)
            gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['armor']
    
    def enemy_ai_update(enemy_head):
        Enemy_body.change_ai()
        # print(game_world.field_array)
        if(enemy_head.x % 60 == 40 and enemy_head.y % 60 == 40):
            Enemy_body.enemy_direction = enemy_ai(Enemy_body.enemy_direction, \
                *coordinates_to_grid(enemy_head.x, enemy_head.y), \
                gw.field_array, Enemy_body.ai)

    def reset():
        Enemy_body.enemy_direction = 0
        Enemy_body.enemy_order = 0
        Enemy_body.bomb_cool_down = 500 // 5
        Enemy_body.enemy_hp = 960 // 900
        Enemy_body.armored = []
        Enemy_body.ai = 0
        Enemy_body.bomb_type = 0
        Enemy_body.damaged = 0

    def change_ai():
        Enemy_body.ai = \
            AI_DICT[(Enemy_body.enemy_hp // 241, COLOR_DICT2[Enemy_body.color])]
        if Enemy_body.color == 'purple':
            if Enemy_body.enemy_hp // 241 == 3:
                Enemy_body.bomb_type = 1
            elif Enemy_body.enemy_hp // 241 == 2:
                Enemy_body.bomb_type = 2
            elif Enemy_body.enemy_hp // 241 == 1:
                Enemy_body.bomb_type = 3
            elif Enemy_body.enemy_hp // 241 == 0:
                Enemy_body.bomb_type = 4

    def enemy_set_bomb():
        if Enemy_body.bomb_cool_down > 0:
            return
        bx, by = Enemy_body.tx, Enemy_body.ty
        gw.addleft_object(bomb(bx, by, 0, \
            choice(bomb_type_list[Enemy_body.bomb_type])), 'bomb')
        Enemy_body.bomb_cool_down = 200

    def check_col(self):
        cur_loc = gw.field_array[self.gx+1][self.gy+1]
        if cur_loc & (FIELD_DICT['player']):
            import module_object.snake_player_obj as sp
            sp.Blue_body.get_damaged()