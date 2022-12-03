from collections import deque
from pico2d import *
from random import choice
from module_object.bomb import Bomb
from module_enemy_ai.enemy_movement_ai import *
from module_other.coordinates_module import *
import module_other.game_world as gw
import module_other.game_framework as gf
import module_other.sound_manager as sm
from module_object.screen_hider import *
from module_other.term_table import *
from module_other.event_table_module import *

COLOR_DICT = {
    STAGE1: 'orange', STAGE2: 'brown',
    STAGE3: 'purple', STAGE4: 'green'
}

AI_DICT = {
    (PHASE1, 'orange'): CIRCLE, (PHASE2, 'orange'): SWEEP,
    (PHASE3, 'orange'): RANDOM, (PHASE4, 'orange'): APPLE_HUNTER,

    (PHASE1, 'brown'): CIRCLE, (PHASE2, 'brown'): SWEEP,
    (PHASE3, 'brown'): RANDOM, (PHASE4, 'brown'): RANDOM,

    (PHASE1, 'purple'): CIRCLE, (PHASE2, 'purple'): RANDOM,
    (PHASE3, 'purple'): CIRCLE, (PHASE4, 'purple'): APPLE_HUNTER,

    (PHASE1, 'green'): SMARTER, (PHASE2, 'green'): BOMB_TOUCH,
    (PHASE3, 'green'): APPLE_DEFENDER, (PHASE4, 'green'): STALKER,
}

PIXEL_PER_MM = (1.0 / 1.6)  # 1 pixel 1.6 mm
MOVE_SPEED_MMPS = 571
MOVE_SPEED_PPS = (MOVE_SPEED_MMPS * PIXEL_PER_MM)

MOVE_PIXEL_PER_A_TIME = 10
UNIT_TIME = 1.0 / (MOVE_SPEED_MMPS * PIXEL_PER_MM / MOVE_PIXEL_PER_A_TIME)

ENEMY_MAX_HP = 960

BOMB_PROBABILITY_DICT = {
    GENERAL_BOMB:
        {PHASE1: 500, PHASE2: 500, PHASE3: 333, PHASE4: 125},
    CROSS_BOMB:
        {PHASE1: 500, PHASE2: 250, PHASE3: 167, PHASE4: 125},
    ICE_CROSS_BOMB:
        {PHASE1: 0, PHASE2: 250, PHASE3: 167, PHASE4: 375},
    ICE_BOMB:
        {PHASE1: 0, PHASE2: 0, PHASE3: 333, PHASE4: 375}
}

class MOVE:
    def do(self):
        self.cumulative_time += gf.elapsed_time
        move_times = int(self.cumulative_time > UNIT_TIME)
        self.cumulative_time = self.cumulative_time % UNIT_TIME
        if self.bomb_cool_down > 0: self.bomb_cool_down -= gf.elapsed_time
        if self.invincible_timer > 0: self.invincible_timer -= gf.elapsed_time
        if self.screen_off_cool_down > 0: self.screen_off_cool_down -= gf.elapsed_time
        if move_times > 0:
            self.unable_to_receive_order = False
            for _ in range(move_times):
                self.bodies_pos[-1][0] = \
                    self.bodies_pos[0][0] + dx[self.cur_state.direction]
                self.bodies_pos[-1][1] = \
                    self.bodies_pos[0][1] + dy[self.cur_state.direction]
                self.bodies_pos.rotate(1)

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
    def delete_from_server(self):
        sv.enemy_head = None

class Enemy:
    img_head = None
    img_body = None
    def __init__(self, stage):
        self.color = COLOR_DICT[stage]
        self.cumulative_time = 0.0
        self.invincible_timer = 0.0
        self.bodies_pos = deque()
        start_pos = list(grid_to_coordinates(0, 8))
        self.bodies_pos += [start_pos.copy() for _ in range(6*(6-1)+1)]
        self.length = 6*(6-1)+1
        self.hp = ENEMY_MAX_HP
        self.bomb_cool_down = 7.0
        self.screen_off_cool_down = 0.0
        self.unable_to_receive_order = False
        self.cur_state = MOVE_RIGHT
        self.damaged = 0
        self.phase = PHASE1
        self.screen_break_cnt = 0
        self.bomb_type = GENERAL_BOMB
        self.get_image()
    def draw(self):
        img = None
        for i in range(-1, -self.length-1, -1):
            img = Enemy.img_head[self.cur_state.direction] \
                if (i == -self.length) else Enemy.img_body
            img.draw(*self.bodies_pos[i])
            gx, gy = coordinates_to_grid(*self.bodies_pos[i])
            gw.field_array[gx+1][gy+1] |= FIELD_DICT['enemy']
    def update(self):
        self.activate_enemy_ability()
        if self.bomb_cool_down <= 0:
            self.set_bomb()
        if self.damaged:
            self.reduce_hp()
            if self.hp <= 0:
                game_clear()
        self.unable_to_receive_order = True
        self.cur_state.do(self)
        if self.bodies_pos[0][0] % 60 != 40 \
            or self.bodies_pos[0][1] % 60 != 40 \
                or self.unable_to_receive_order:
            return
        ai = AI_DICT[(self.phase, self.color)]
        self.cur_state = next_state[get_order_from_enemy_ai(ai)]

    def handle_collision(self, other, group):
        if group == COL_EHEAD_APPLE:
            sm.sound_effect.play(SE_EAT)
        elif group == COL_EXPLOSION_ENEMY:
            if self.invincible_timer <= 0:
                self.get_damaged(other.damage)
        
    def get_phase_num(self):
        if self.hp > ENEMY_MAX_HP * 0.75: return PHASE1
        if self.hp > ENEMY_MAX_HP * 0.50: return PHASE2
        if self.hp > ENEMY_MAX_HP * 0.25: return PHASE3
        else: return PHASE4

    def get_image(self):
        Enemy.img_head = [load_image('img/snake_' + self.color + '_head_' \
            + str(i) + '.png') for i in range(4)]
        Enemy.img_body = load_image('img/snake_' + self.color + '_body.png')

    def get_damaged(self, damage):
        if damage == 0: return
        self.damaged = max(self.damaged, damage)

    def reduce_hp(self):
        self.invincible_timer += 0.15
        self.hp -= self.damaged
        self.phase = self.get_phase_num()
        self.damaged = 0

    def set_bomb(self):
        bx, by = self.bodies_pos[-1]
        sv.bomb.appendleft(Bomb(bx, by, 0, self.bomb_type))
        gw.addleft_object(sv.bomb[0], 'bomb')
        self.bomb_cool_down = 7.0

    def activate_enemy_ability(self):
        if self.color == 'brown':
            if self.phase >= PHASE4 and self.screen_off_cool_down <= 0:
                self.turn_off_screen()
            if self.phase >= PHASE3 and sv.cloud == None:
                sv.cloud = Cloud()
                gw.addleft_object(sv.cloud, 'hider')
            if self.screen_break_cnt != self.phase:
                self.screen_break_cnt += 1
                sv.broken.append(Broken())
                gw.add_object(sv.broken[-1], 'hider')
        elif self.color == 'purple':
            if self.bomb_cool_down > 0: return
            self.bomb_type = self.get_bomb_type()
        elif self.color == 'green':
            if self.bomb_cool_down > 4.2:
                self.bomb_cool_down = 4.2

    def turn_off_screen(self):
        self.screen_off_cool_down = 10.0
        sv.screen_off = Screen_off()
        gw.add_object(sv.screen_off, 'hider')

    def get_bomb_type(self):
        random_number = randint(1, 1000)
        for bomb_type in BOMB_TYPES:
            prob = BOMB_PROBABILITY_DICT[bomb_type][self.phase]
            if random_number <= prob:
                return bomb_type
            random_number -= prob
        return GENERAL_BOMB

    def delete_from_server(self):
        sv.enemy = None

def game_clear():
    import module_state.play_state as ps
    ps.isended = VICTORY

next_state = {
    RIGHT: MOVE_RIGHT, LEFT: MOVE_LEFT, UP: MOVE_UP, DOWN: MOVE_DOWN
}