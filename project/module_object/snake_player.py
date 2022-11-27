from pico2d import *
from module_other.coordinates_module import *
from collections import deque
from module_other.term_table import *
from module_other.event_table_module import *
from module_object.bomb import *
from module_object.mine import *
from module_object.apple import *
from module_object.skin_wall import *
import module_other.game_world as gw
import module_other.sound_manager as sm
import module_other.game_framework as gf

LENGTH_PER_GRID = 6
MAX_GRID = 10
MIN_GRID = 2
MAX_LENGTH = LENGTH_PER_GRID * (MAX_GRID - 1) + 1
MIN_LENGTH = LENGTH_PER_GRID * (MIN_GRID - 1) + 1

PIXEL_PER_MM = (1.0 / 1.6)  # 1 pixel 1.6 mm
MOVE_SPEED_MMPS = 571
MOVE_SPEED_PPS = (MOVE_SPEED_MMPS * PIXEL_PER_MM)

MOVE_PIXEL_PER_A_TIME = 10
UNIT_TIME = 1.0 / (MOVE_SPEED_MMPS * PIXEL_PER_MM / MOVE_PIXEL_PER_A_TIME)

class MOVE:
    def enter(self, event):
        pass
    def exit(self, event):
        if event == KED:
            if self.bomb_cool_down <= 0:
                bx, by = self.bodies_pos[-1]
                sv.bomb.appendleft(Bomb(bx, by, self.length))
                gw.addleft_object(sv.bomb[0], 'bomb')
                self.bomb_cool_down = 1

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

class MOVE_RIGHT(MOVE):
    direction = RIGHT

class MOVE_UP(MOVE):
    direction = UP

class MOVE_LEFT(MOVE):
    direction = LEFT

class MOVE_DOWN(MOVE):
    direction = DOWN

class Player_head:
    def __init__(self):
        self.x, self.y = 0, 0
    def update(self):
        self.x, self.y = sv.player.bodies_pos[0]
    def draw(self):
        pass
    def handle_collision(self, other, group):
        sv.player.handle_collision(other, group)
    def delete_from_server(self):
        sv.player_head = None

class Player:
    img_head = None
    img_body = None
    def __init__(self, character):
        self.character = character
        self.cumulative_time = 0.0
        self.invincible_timer = 0.0
        self.bodies_pos = deque()
        start_pos = list(grid_to_coordinates(0, 0))
        self.bodies_pos += [start_pos.copy() for _ in range(6*(3-1)+1)]
        self.length = 13
        self.bomb_cool_down = 1.0
        self.unable_to_receive_order = False
        self.event_que = deque(maxlen=2)
        self.cur_state = MOVE_RIGHT
        self.cur_state.enter(self, None)
        if Player.img_head == None: get_image()
    def draw(self):
        img = None
        for i in range(-1, -self.length-1, -1):
            img = Player.img_head[self.cur_state.direction] \
                if (i == -self.length) else Player.img_body
            img.draw(*self.bodies_pos[i])
            gx, gy = coordinates_to_grid(*self.bodies_pos[i])
            gw.field_array[gx+1][gy+1] |= FIELD_DICT['player']
    def update(self):
        self.unable_to_receive_order = True
        self.cur_state.do(self)
        if self.event_que:
            if self.event_que[-1] != KED:
                if self.bodies_pos[0][0] % 60 != 40 \
                    or self.bodies_pos[0][1] % 60 != 40 \
                        or self.unable_to_receive_order:
                    return
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)
    def get_longer(self):
        self.create_byproduct()
        if self.length >= MAX_LENGTH:
            return
        self.length += 6
        tail_pos = self.bodies_pos[-1]
        self.bodies_pos += [tail_pos.copy() for _ in range(6)]
    def get_shorter(self):
        if self.length <= MIN_LENGTH:
            game_over()
            return
        self.length -= 6
        for _ in range(6):
            self.bodies_pos.pop()

    def handle_collision(self, other, group):
        if group == COL_PHEAD_APPLE:
            sm.sound_effect.play(SE_EAT)
            if type(other) == Poison_apple:
                self.get_shorter()
            else:
                self.get_longer()
        elif group == COL_PLAYER_EHEAD:
            self.get_shorter()
        elif group in (COL_PHEAD_ENEMY, COL_PHEAD_WALL):
            game_over()
        elif group in (COL_EXPLOSION_PLAYER, COL_PLAYER_ICE):
            if self.invincible_timer <= 0:
                self.get_shorter()
                self.invincible_timer += 0.15

    def add_event(self, event):
        self.event_que.appendleft(event)

    def handle_events(self, event):
        if event in EVENT_SNAKE_HANDLES:
            self.add_event(event)

    def create_byproduct(self):
        if self.character == MINE_SWEEPER_SNAKE:
            sv.mine.append(Mine())
            gw.add_object(sv.mine[-1], 'obj')
        elif self.character == SKIN_SHEDDER_SNAKE:
            for i in range(self.length - 1, 12, -1):
                sv.skin_wall.append(Skin_wall(*self.bodies_pos[i]))
                gw.add_object(sv.skin_wall[-1], 'breakable')

    def delete_from_server(self):
        sv.player = None

def game_over():
    import module_state.play_state as ps
    ps.isended = DEFEAT

def get_image():
    Player.img_head = [load_image('img/snake_blue_head_' + str(i) + '.png')\
        for i in range(4)]
    Player.img_body = load_image('img/snake_blue_body.png')

next_state = {
    MOVE_RIGHT: {KDD: MOVE_RIGHT, KWD: MOVE_UP,
        KAD: MOVE_RIGHT, KSD: MOVE_DOWN, KED: MOVE_RIGHT},
    MOVE_UP: {KDD: MOVE_RIGHT, KWD: MOVE_UP,
        KAD: MOVE_LEFT, KSD: MOVE_UP, KED: MOVE_UP},
    MOVE_LEFT: {KDD: MOVE_LEFT, KWD: MOVE_UP,
        KAD: MOVE_LEFT, KSD: MOVE_DOWN, KED: MOVE_LEFT},
    MOVE_DOWN: {KDD: MOVE_RIGHT, KWD: MOVE_DOWN,
        KAD: MOVE_LEFT, KSD: MOVE_DOWN, KED: MOVE_DOWN}
}