from module_other.coordinates_module import *
from collections import deque
from pico2d import *
from random import choice
from module_object.bomb import Bomb
from module_enemy_ai.enemy_movement_ai import enemy_ai
import module_other.game_world as gw
from module_object.screen_hider import *
import module_other.bgm_player as bp
from module_other.term_table import *

COLOR_DICT = {'1': 'orange', '2': 'brown', '3': 'purple', '4': 'green'}
COLOR_DICT2 = {'orange': 1, 'brown': 2, 'purple': 3, 'green': 4}

AI_DICT = {
    (PHASE[1], ORANGE): CIRCLE, (PHASE[2], ORANGE): SWEEP,
    (PHASE[3], ORANGE): RANDOM, (PHASE[4], ORANGE): APPLE_HUNTER,

    (PHASE[1], BROWN): CIRCLE, (PHASE[2], BROWN): SWEEP,
    (PHASE[3], BROWN): RANDOM, (PHASE[4], BROWN): RANDOM,

    (PHASE[1], PURPLE): CIRCLE, (PHASE[2], PURPLE): RANDOM,
    (PHASE[3], PURPLE): CIRCLE, (PHASE[4], PURPLE): APPLE_HUNTER,

    (PHASE[1], GREEN): SMARTER, (PHASE[2], GREEN): BOMB_TOUCH,
    (PHASE[3], GREEN): APPLE_DEFENDER, (PHASE[4], GREEN): STALKER,
}

BOMB_TYPE_DICT = {
    0: (0,),
    1: (0, 1),
    2: (0, 0, 1, 3),
    3: (0, 0, 1, 3, 2, 2),
    4: (3, 3, 3, 2, 2, 2, 1, 0)
}

def get_image(color):
    img_head = [load_image('img/snake_' + color + '_head_' + str(i) + '.png') \
        for i in range(4)]
    img_body = load_image('img/snake_' + color + '_body.png')
    return img_head, img_body

class Enemy_body:
    enemy_direction = 0
    enemy_order = 0
    bomb_cool_down = 500
    screen_off_cool_down = 400
    enemy_hp = 960
    color = None
    img_head = None
    img_body = None
    ai = 0
    bomb_type = 0
    length = 12*(6-1)+1
    hx, hy = grid_to_coordinates(0, 8)
    tx, ty = hx, hy
    damaged = 0
    screen_break_cnt = 0
    cloud_cnt = 0
    bgm = None
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
        if Enemy_body.img_body == None:
            Enemy_body.img_head, Enemy_body.img_body = \
                get_image(Enemy_body.color)
        if Enemy_body.bgm == None:
            Enemy_body.bgm = bp.Stage_bgm(COLOR_DICT2[self.color])
    def get_damaged(damage):
        if Enemy_body.damaged < damage:
            Enemy_body.damaged = damage
    def update(self):
        if(self.number == self.length - 1):
            self.x, self.y = Enemy_body.hx + dx[Enemy_body.enemy_direction], \
                Enemy_body.hy + dy[Enemy_body.enemy_direction]
            self.number = 0
            if Enemy_body.bomb_cool_down > 0: Enemy_body.bomb_cool_down -= 1
            if Enemy_body.screen_off_cool_down > 0: Enemy_body.screen_off_cool_down -= 1
            if Enemy_body.damaged:
                Enemy_body.enemy_hp -= Enemy_body.damaged
                Enemy_body.damaged = 0
        else:
            if(self.number == 0):
                self.enemy_ai_update()
            self.number += 1
        if Enemy_body.enemy_hp <= 0:
            Enemy_body.enemy_hp = 0
            import module_state.play_state as ps
            ps.isended = VICTORY

    def draw(self):
        self.gx, self.gy = coordinates_to_grid(self.x, self.y)
        self.image = Enemy_body.img_body
        if(self.number == 0):
            gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['ehead']
            Enemy_body.hx, Enemy_body.hy = self.x, self.y
            return
        else:
            if(self.number == self.length-1):
                Enemy_body.tx, Enemy_body.ty = self.x, self.y
        self.image.draw(self.x, self.y)
        if(self.number == self.length - 1):
            Enemy_body.img_head\
                [Enemy_body.enemy_direction].draw(Enemy_body.hx, Enemy_body.hy)
        gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['enemy']
    
    def enemy_ai_update(enemy_head):
        Enemy_body.change_ai()
        # print(game_world.field_array)
        if(enemy_head.x % 60 == 40 and enemy_head.y % 60 == 40):
            Enemy_body.enemy_direction = enemy_ai(Enemy_body.enemy_direction, \
                *coordinates_to_grid(enemy_head.x, enemy_head.y), \
                gw.field_array, Enemy_body.ai)

    def reset():
        Enemy_body.color = None
        Enemy_body.img_body = None
        Enemy_body.img_head = None
        Enemy_body.enemy_direction = 0
        Enemy_body.enemy_order = 0
        Enemy_body.bomb_cool_down = 500
        Enemy_body.screen_off_cool_down = 0
        Enemy_body.enemy_hp = 960 // 1
        Enemy_body.ai = 0
        Enemy_body.bomb_type = 0
        Enemy_body.damaged = 0
        Enemy_body.screen_break_cnt = 0
        Enemy_body.cloud_cnt = 0
        if Enemy_body.bgm != None:
            Enemy_body.bgm.stops()
            Enemy_body.bgm = None

    def change_ai():
        Enemy_body.ai = \
            AI_DICT[(Enemy_body.enemy_hp // 241, COLOR_DICT2[Enemy_body.color])]
        if Enemy_body.color == 'purple':
            Enemy_body.bomb_type = 4 - Enemy_body.enemy_hp // 241
        elif Enemy_body.color == 'brown':
            screen_break(3 - Enemy_body.enemy_hp // 241)

    def enemy_set_bomb():
        if Enemy_body.bomb_cool_down > 0:
            return
        bx, by = Enemy_body.tx, Enemy_body.ty
        gw.addleft_object(Bomb(bx, by, 0, \
            choice(BOMB_TYPE_DICT[Enemy_body.bomb_type])), 'bomb')
        Enemy_body.bomb_cool_down = 200

    def create_cloud():
        if Enemy_body.color != 'brown':
            return
        if Enemy_body.enemy_hp // 241 > 1:
            return
        if Enemy_body.cloud_cnt != 0:
            return
        Enemy_body.cloud_cnt += 1
        gw.addleft_object(Cloud(), 'hider')

    def enemy_screen_off():
        if Enemy_body.color != 'brown':
            return
        if Enemy_body.enemy_hp // 241 > 0:
            return
        if Enemy_body.screen_off_cool_down > 0:
            return
        gw.add_object(Screen_off(), 'hider')
        Enemy_body.screen_off_cool_down = 700

    def check_col(self):
        cur_loc = gw.field_array[self.gx+1][self.gy+1]
        if cur_loc & (FIELD_DICT['player']):
            import module_object.snake_player as sp
            sp.Blue_body.get_damaged()

def screen_break(hp):
    if Enemy_body.screen_break_cnt != hp:
        return
    Enemy_body.screen_break_cnt += 1
    gw.add_object(Broken(), 'hider')