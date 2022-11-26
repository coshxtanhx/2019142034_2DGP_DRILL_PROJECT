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

class MOVE:
    def enter(self, event):
        pass
    def exit(self, event):
        if event == KED:
            if self.bomb_cool_down <= 0:
                bx, by = self.bodies_pos[-1]
                gw.addleft_object(Bomb(bx, by, self.length), 'bomb')
                self.bomb_cool_down = 1

    def do(self):
        self.cumulative_time += gf.elapsed_time
        move_times = int(self.cumulative_time / 0.028)
        self.cumulative_time = self.cumulative_time % 0.028
        if self.bomb_cool_down > 0: self.bomb_cool_down -= gf.elapsed_time
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
        self.bomb_cool_down = 0.0
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

    def handle_collision(self, other, group):
        if group == COL_PHEAD_APPLE:
            sm.sound_effect.play(SE_EAT)
            if type(other) == Poison_apple:
                pass
            else:
                self.length += 6
                tail_pos = self.bodies_pos[-1]
                self.bodies_pos += [tail_pos.copy() for _ in range(6)]
        elif group in (COL_PLAYER_EHEAD, COL_PLAYER_ICE):
            pass
        elif group == COL_EXPLOSION_PLAYER:
            if self.invincible_timer <= 0:
                pass
                self.invincible_timer += 0.15

    def add_event(self, event):
        self.event_que.appendleft(event)

    def handle_events(self, event):
        if event in EVENT_SNAKE_HANDLES:
            self.add_event(event)

'''
class Player_body:
    invincible_timer = None
    img_snake_blue_head = None
    img_snake_blue_body = None
    character = None
    cur_direction = 0
    damaged = False
    longer = False
    skinshed = False
    direction = deque(maxlen=2)
    move_times = 0
    rest_time = 0
    bomb_cool_down = 1
    length = 12*(3-1)+1
    hx, hy = convert_coordinates(40, 120)
    tx, ty = hx, hy
    def __init__(self, number, x=40, y=-1):
        if(y == -1):
            self.x, self.y = convert_coordinates(x, 120)
        else:
            self.x, self.y = x, y
        self.gx, self.gy = coordinates_to_grid(self.x, self.y)
        self.frame = 0
        self.number = number
        self.image = 0
        if(Player_body.img_snake_blue_head == None):
            Player_body.img_snake_blue_head = \
                [load_image('img/snake_blue_head_' + str(i) + '.png')\
                    for i in range(4)]
            Player_body.img_snake_blue_body = load_image('img/snake_blue_body.png')
    def update(self):
        if(self.number == self.length - Player_body.move_times):
            self.x = Player_body.hx + dx[Player_body.cur_direction]
            self.y = Player_body.hy + dy[Player_body.cur_direction]
            Player_body.hx, Player_body.hy = self.x, self.y
            Player_body.skinshed = False
        else:
            if(self.number == 0):
                Player_body.rest_time += gf.elapsed_time
                Player_body.move_times = int(Player_body.rest_time / 0.014)
                Player_body.rest_time = Player_body.rest_time % 0.014
                Player_body.bomb_cool_down -= gf.elapsed_time
                if Player_body.invincible_timer > 0:
                    Player_body.invincible_timer -= gf.elapsed_time
                if(Player_body.direction and self.x % 60 == 40 and self.y % 60 == 40):
                    Player_body.cur_direction = \
                        next_state[Player_body.cur_direction][Player_body.direction.pop()]
        self.number = (self.number + Player_body.move_times) % Player_body.length
        if self.number > 30 and Player_body.skinshed:
            gw.add_object(Skin_wall(self.x, self.y), 'breakable')
    def get_longer():
        if Player_body.longer == False:
            return
        Player_body.longer = False
        for i in range(12):
            gw.add_object(Player_body(Player_body.length+i, \
                Player_body.tx, Player_body.ty), 'player')
        Player_body.length += 12
        if Player_body.character == MINE_SWEEPER_SNAKE:
            gw.add_object(Mine(), 'obj')
        if Player_body.character == SKIN_SHEDDER_SNAKE:
            Player_body.skinshed = True
    def get_shorter():
        if Player_body.damaged == False:
            return
        Player_body.damaged = False
        if Player_body.length < 15:
            game_over()
        else:
            Player_body.length -= 12
            for _ in range(12):
                gw.pop_object('player')
    def draw(self):
        self.gx, self.gy = coordinates_to_grid(self.x, self.y)
        if(self.number == 0):
            gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['head']
            return
        else:
            if(self.number > 30):
                gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['body']
            self.image = Player_body.img_snake_blue_body
            if(self.number == self.length-1):
                Player_body.tx, Player_body.ty = self.x, self.y
        self.image.draw(self.x, self.y)
        gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['player']
        if(self.number == self.length - 1):
            (Player_body.img_snake_blue_head[Player_body.cur_direction]\
                ).draw(Player_body.hx, Player_body.hy)
    def get_damaged():
        Player_body.damaged = True
    def reset():
        Player_body.cur_direction = 0
        Player_body.direction = deque(maxlen=2)
        Player_body.bomb_cool_down = 0
        Player_body.length = 12*(3-1)+1
        Player_body.move_times = 0
        Player_body.rest_time = 0
        Player_body.hx, Player_body.hy = convert_coordinates(40, 120)
        Player_body.invincible_timer = 0.0

    def handle_events(event):
        if event in next_state[Player_body.cur_direction]:
            if event == KED:
                if Player_body.bomb_cool_down <= 0:
                    bx, by = Player_body.tx, Player_body.ty
                    gw.addleft_object(Bomb(bx, by, Player_body.length), 'bomb')
                    Player_body.bomb_cool_down = 1
            else:
                Player_body.direction.appendleft(event)
    
    def handle_collision(self, other, group):
        if group == COL_PLAYER_APPLE:
            sm.sound_effect.play(SE_EAT)
            if type(other) == Poison_apple:
                Player_body.get_damaged()
            else: Player_body.longer = True
        elif group in (COL_PLAYER_ENEMY, COL_PLAYER_ICE):
            Player_body.get_damaged()
        elif group == COL_EXPLOSION_PLAYER:
            if Player_body.invincible_timer <= 0:
                Player_body.get_damaged()
                Player_body.invincible_timer += 0.15
'''

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