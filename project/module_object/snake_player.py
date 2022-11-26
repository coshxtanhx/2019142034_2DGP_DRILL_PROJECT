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
        # cur_loc = gw.field_array[self.gx+1][self.gy+1]
        # if Player_body.length >= 40 and \
        #     (cur_loc & (FIELD_DICT['body']+FIELD_DICT['head']) \
        #         == (FIELD_DICT['body']+FIELD_DICT['head'])):
        #     game_over()
        # if cur_loc & (FIELD_DICT['wall']):
        #     game_over()
        # if cur_loc & (FIELD_DICT['apple']):
        #     Player_body.longer = True
        # if cur_loc & (FIELD_DICT['poison']):
        #     Player_body.get_damaged()


def game_over():
    import module_state.play_state as ps
    ps.isended = DEFEAT

GO_D, GO_W, GO_A, GO_S = range(4)
next_state = {
    GO_D: {KDD: GO_D, KWD: GO_W, KAD: GO_D, KSD: GO_S, KED: GO_D},
    GO_W: {KDD: GO_D, KWD: GO_W, KAD: GO_A, KSD: GO_W, KED: GO_W},
    GO_A: {KDD: GO_A, KWD: GO_W, KAD: GO_A, KSD: GO_S, KED: GO_A},
    GO_S: {KDD: GO_D, KWD: GO_S, KAD: GO_A, KSD: GO_S, KED: GO_S}
}