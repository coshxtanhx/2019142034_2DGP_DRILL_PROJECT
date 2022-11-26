from module_other.coordinates_module import *
from collections import deque
from pico2d import *
from random import choice
from module_object.bomb import Bomb
from module_enemy_ai.enemy_movement_ai import enemy_ai
import module_other.game_world as gw
import module_other.game_framework as gf
import module_other.sound_manager as sm
from module_object.screen_hider import *
from module_other.term_table import *
from module_other.event_table_module import *

COLOR_DICT = {'1': 'orange', '2': 'brown', '3': 'purple', '4': 'green'}

AI_DICT = {
    (PHASE[1], 'orange'): CIRCLE, (PHASE[2], 'orange'): SWEEP,
    (PHASE[3], 'orange'): RANDOM, (PHASE[4], 'orange'): APPLE_HUNTER,

    (PHASE[1], 'brown'): CIRCLE, (PHASE[2], 'brown'): SWEEP,
    (PHASE[3], 'brown'): RANDOM, (PHASE[4], 'brown'): RANDOM,

    (PHASE[1], 'purple'): CIRCLE, (PHASE[2], 'purple'): RANDOM,
    (PHASE[3], 'purple'): CIRCLE, (PHASE[4], 'purple'): APPLE_HUNTER,

    (PHASE[1], 'green'): SMARTER, (PHASE[2], 'green'): BOMB_TOUCH,
    (PHASE[3], 'green'): APPLE_DEFENDER, (PHASE[4], 'green'): STALKER,
}

BOMB_TYPE_DICT = {
    0: (0,),
    1: (0, 1),
    2: (0, 0, 1, 3),
    3: (0, 0, 1, 3, 2, 2),
    4: (3, 3, 3, 2, 2, 2, 1, 0)
}

PIXEL_PER_MM = (1.0 / 1.6)  # 1 pixel 1.6 mm
MOVE_SPEED_MMPS = 571
MOVE_SPEED_PPS = (MOVE_SPEED_MMPS * PIXEL_PER_MM)

MOVE_PIXEL_PER_A_TIME = 10
UNIT_TIME = 1.0 / (MOVE_SPEED_MMPS * PIXEL_PER_MM / MOVE_PIXEL_PER_A_TIME)

class MOVE:
    def do(self):
        self.cumulative_time += gf.elapsed_time
        move_times = int(self.cumulative_time / UNIT_TIME)
        self.cumulative_time = self.cumulative_time % UNIT_TIME
        if self.bomb_cool_down > 0: self.bomb_cool_down -= gf.elapsed_time
        if self.invincible_timer > 0: self.invincible_timer -= gf.elapsed_time
        if move_times > 0:
            self.unable_to_receive_order = False
            for i in range(-1, -1-move_times, -1):
                self.bodies_pos[i][0] = \
                    self.bodies_pos[0][0] + dx[self.cur_state.direction]
                self.bodies_pos[i][1] = \
                    self.bodies_pos[0][1] + dy[self.cur_state.direction]
                self.bodies_pos.rotate(1)
        if self.bomb_cool_down <= 0:
            bx, by = self.bodies_pos[-1]
            sv.bomb.append(Bomb(bx, by, 0))
            gw.addleft_object(sv.bomb[-1], 'bomb')
            self.bomb_cool_down = 1.4

class MOVE_RIGHT(MOVE):
    direction = RIGHT

class MOVE_UP(MOVE):
    direction = UP

class MOVE_LEFT(MOVE):
    direction = LEFT

class MOVE_DOWN(MOVE):
    direction = DOWN

class Enemy_head:
    def __init__(self):
        self.x, self.y = 0, 0
    def update(self):
        self.x, self.y = sv.enemy.bodies_pos[0]
    def draw(self):
        pass
    def handle_collision(self, other, group):
        sv.enemy.handle_collision(other, group)

class Enemy:
    img_head = None
    img_body = None
    def __init__(self, color):
        self.color = color
        self.cumulative_time = 0.0
        self.invincible_timer = 0.0
        self.bodies_pos = deque()
        start_pos = list(grid_to_coordinates(0, 8))
        self.bodies_pos += [start_pos.copy() for _ in range(6*(6-1)+1)]
        self.length = 31
        self.bomb_cool_down = 0.0
        self.unable_to_receive_order = False
        self.event_que = deque(maxlen=1)
        self.cur_state = MOVE_RIGHT
        self.cur_state.enter(self, None)
        if Enemy.img_head == None: get_image()
    def draw(self):
        img = None
        for i in range(-1, -self.length-1, -1):
            img = Enemy.img_head[self.cur_state.direction] \
                if (i == -self.length) else Enemy.img_body
            img.draw(*self.bodies_pos[i])
            gx, gy = coordinates_to_grid(*self.bodies_pos[i])
            gw.field_array[gx+1][gy+1] |= FIELD_DICT['enemy']
    def update(self):
        self.unable_to_receive_order = True
        self.cur_state.do(self)
        if self.bodies_pos[0][0] % 60 != 40 \
            or self.bodies_pos[0][1] % 60 != 40 \
                or self.unable_to_receive_order:
            return
        # fill here
        self.cur_state = next_state[enemy_ai(0)]

    def handle_collision(self, other, group):
        if group == COL_EHEAD_APPLE:
            sm.sound_effect.play(SE_EAT)
        elif group == COL_EXPLOSION_ENEMY:
            if self.invincible_timer <= 0:
                pass
                self.invincible_timer += 0.15

# class Enemy_body:
#     invincible_timer = None
#     enemy_direction = 0
#     enemy_order = 0
#     bomb_cool_down = 500
#     screen_off_cool_down = 400
#     enemy_hp = 960
#     color = None
#     img_head = None
#     img_body = None
#     ai = 0
#     bomb_type = 0
#     length = 12*(6-1)+1
#     hx, hy = grid_to_coordinates(0, 8)
#     tx, ty = hx, hy
#     damaged = 0
#     move_times = 0
#     rest_time = 0
#     screen_break_cnt = 0
#     cloud_cnt = 0
#     def __init__(self, number, color = 'orange', x=40, y=-1):
#         if(y == -1):
#             self.x, self.y = grid_to_coordinates(0, 8)
#         else:
#             self.x, self.y = x, y
#         self.gx, self.gy = coordinates_to_grid(self.x, self.y)
#         self.frame = 0
#         self.number = number
#         self.image = 0
#         Enemy_body.color = color
#         if Enemy_body.img_body == None:
#             Enemy_body.img_head, Enemy_body.img_body = \
#                 get_image(Enemy_body.color)
#     def get_damaged(damage):
#         if Enemy_body.damaged < damage:
#             Enemy_body.damaged = damage
#     def update(self):
#         if(self.number == self.length - Enemy_body.move_times):
#             self.x, self.y = Enemy_body.hx + dx[Enemy_body.enemy_direction], \
#                 Enemy_body.hy + dy[Enemy_body.enemy_direction]
#             Enemy_body.hx, Enemy_body.hy = self.x, self.y
#             if Enemy_body.damaged:
#                 Enemy_body.enemy_hp -= Enemy_body.damaged
#                 Enemy_body.damaged = 0
#         else:
#             if(self.number == 0):
#                 Enemy_body.rest_time += gf.elapsed_time
#                 Enemy_body.move_times = int(Enemy_body.rest_time / 0.014)
#                 Enemy_body.rest_time = Enemy_body.rest_time % 0.014
#                 Enemy_body.bomb_cool_down -= gf.elapsed_time
#                 Enemy_body.invincible_timer -= gf.elapsed_time
#                 Enemy_body.screen_off_cool_down -= gf.elapsed_time
#                 self.enemy_ai_update()
#         self.number = (self.number + Enemy_body.move_times) % Enemy_body.length
#         if Enemy_body.enemy_hp <= 0:
#             Enemy_body.enemy_hp = 0
#             import module_state.play_state as ps
#             ps.isended = VICTORY
#         Enemy_body.enemy_set_bomb()
#         Enemy_body.enemy_screen_off()
#         Enemy_body.create_cloud()

#     def draw(self):
#         self.gx, self.gy = coordinates_to_grid(self.x, self.y)
#         self.image = Enemy_body.img_body
#         if(self.number == 0):
#             gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['ehead']
#             return
#         else:
#             if(self.number == self.length-1):
#                 Enemy_body.tx, Enemy_body.ty = self.x, self.y
#         self.image.draw(self.x, self.y)
#         if(self.number == self.length - 1):
#             Enemy_body.img_head\
#                 [Enemy_body.enemy_direction].draw(Enemy_body.hx, Enemy_body.hy)
#         gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['enemy']
    
#     def enemy_ai_update(enemy_head):
#         Enemy_body.change_ai()
#         # print(game_world.field_array)
#         if(enemy_head.x % 60 == 40 and enemy_head.y % 60 == 40):
#             Enemy_body.enemy_direction = enemy_ai(Enemy_body.enemy_direction, \
#                 *coordinates_to_grid(enemy_head.x, enemy_head.y), \
#                 gw.field_array, Enemy_body.ai)

#     def reset():
#         Enemy_body.invincible_timer = 0.0
#         Enemy_body.color = None
#         Enemy_body.img_body = None
#         Enemy_body.img_head = None
#         Enemy_body.enemy_direction = 0
#         Enemy_body.enemy_order = 0
#         Enemy_body.bomb_cool_down = 7.5
#         Enemy_body.screen_off_cool_down = 0
#         Enemy_body.enemy_hp = 960 // 1
#         Enemy_body.ai = 0
#         Enemy_body.bomb_type = 0
#         Enemy_body.damaged = 0
#         Enemy_body.move_times = 0
#         Enemy_body.rest_time = 0
#         Enemy_body.screen_break_cnt = 0
#         Enemy_body.cloud_cnt = 0
#         Enemy_body.hx, Enemy_body.hy = grid_to_coordinates(0, 8)

#     def change_ai():
#         Enemy_body.ai = \
#             AI_DICT[(Enemy_body.enemy_hp // 241, Enemy_body.color)]
#         if Enemy_body.color == 'purple':
#             Enemy_body.bomb_type = 4 - Enemy_body.enemy_hp // 241
#         elif Enemy_body.color == 'brown':
#             screen_break(3 - Enemy_body.enemy_hp // 241)

#     def enemy_set_bomb():
#         if Enemy_body.bomb_cool_down > 0:
#             return
#         bx, by = Enemy_body.tx, Enemy_body.ty
#         gw.addleft_object(Bomb(bx, by, 0, \
#             choice(BOMB_TYPE_DICT[Enemy_body.bomb_type])), 'bomb')
#         Enemy_body.bomb_cool_down = 7

#     def create_cloud():
#         if Enemy_body.color != 'brown':
#             return
#         if Enemy_body.enemy_hp // 241 > 1:
#             return
#         if Enemy_body.cloud_cnt != 0:
#             return
#         Enemy_body.cloud_cnt += 1
#         gw.addleft_object(Cloud(), 'hider')

#     def enemy_screen_off():
#         if Enemy_body.color != 'brown':
#             return
#         if Enemy_body.enemy_hp // 241 > 0:
#             return
#         if Enemy_body.screen_off_cool_down > 0:
#             return
#         gw.add_object(Screen_off(), 'hider')
#         Enemy_body.screen_off_cool_down = 10

#     def handle_collision(self, other, group):
#         if group == COL_EHEAD_APPLE:
#             sm.sound_effect.play(SE_EAT) 
#         elif group == COL_EXPLOSION_ENEMY:
#             if Enemy_body.invincible_timer <= 0:
#                 Enemy_body.get_damaged(other.damage)
#                 Enemy_body.invincible_timer += 0.15

# def screen_break(hp):
#     if Enemy_body.screen_break_cnt != hp:
#         return
#     Enemy_body.screen_break_cnt += 1
#     gw.add_object(Broken(), 'hider')

def get_image():
    color = sv.enemy.color
    Enemy.img_head = [load_image('img/snake_' + color + '_head_' \
        + str(i) + '.png') for i in range(4)]
    Enemy.img_body = load_image('img/snake_' + color + '_body.png')

next_state = {
    RIGHT: MOVE_RIGHT, LEFT: MOVE_LEFT, UP: MOVE_UP, DOWN: MOVE_DOWN
}