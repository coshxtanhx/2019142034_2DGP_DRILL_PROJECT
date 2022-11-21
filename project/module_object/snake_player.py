from module_other.coordinates_module import *
from collections import deque
from pico2d import *
from module_other.event_table_module import *
from module_object.bomb import Bomb, Skin
from module_object.mine import Mine
import module_other.game_world as gw
import module_other.state_changer as sc

class Blue_body:
    img_snake_blue_head = None
    img_snake_blue_body = None
    character = None
    cur_direction = 0
    damaged = False
    longer = False
    skinshed = False
    direction = deque(maxlen=2)
    bomb_cool_down = 10
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
        if(Blue_body.img_snake_blue_head == None):
            Blue_body.img_snake_blue_head = \
                [load_image('img/snake_blue_head_' + str(i) + '.png')\
                    for i in range(4)]
            Blue_body.img_snake_blue_body = load_image('img/snake_blue_body.png')
    def update(self):
        if(self.number == self.length - 1):
            self.x, self.y = self.hx + dx[Blue_body.cur_direction], \
                self.hy + dy[Blue_body.cur_direction]
            self.number = 0
            if Blue_body.bomb_cool_down > 0: Blue_body.bomb_cool_down -= 1
            Blue_body.skinshed = False
        else:
            if(self.number == 0):
                if(Blue_body.direction and self.x % 60 == 40 and self.y % 60 == 40):
                    Blue_body.cur_direction = \
                        next_state[Blue_body.cur_direction][Blue_body.direction.pop()]
            self.number += 1
        if self.number > 30 and Blue_body.skinshed:
            gw.add_object(Skin(self.x, self.y), 'ice')
    def get_longer():
        if Blue_body.longer == False:
            return
        Blue_body.longer = False
        for i in range(12):
            gw.add_object(Blue_body(Blue_body.length+i, \
                Blue_body.tx, Blue_body.ty), 'player')
        Blue_body.length += 12
        if Blue_body.character == '3':
            gw.add_object(Mine(), 'obj')
        if Blue_body.character == '4':
            Blue_body.skinshed = True
    def get_shorter():
        if Blue_body.damaged == False:
            return
        Blue_body.damaged = False
        if Blue_body.length < 15:
            game_over()
        else:
            Blue_body.length -= 12
            for _ in range(12):
                gw.pop_object('player')
    def draw(self):
        self.gx, self.gy = coordinates_to_grid(self.x, self.y)
        if(self.number == 0):
            gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['head']
            Blue_body.hx, Blue_body.hy = self.x, self.y
            return
        else:
            if(self.number > 30):
                gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['body']
            self.image = Blue_body.img_snake_blue_body
            if(self.number == self.length-1):
                Blue_body.tx, Blue_body.ty = self.x, self.y
        self.image.draw(self.x, self.y)
        gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['player']
        if(self.number == self.length - 1):
            (Blue_body.img_snake_blue_head[Blue_body.cur_direction]\
                ).draw(Blue_body.hx, Blue_body.hy)
    def get_damaged():
        Blue_body.damaged = True
    def reset():
        Blue_body.cur_direction = 0
        Blue_body.direction = deque(maxlen=2)
        Blue_body.bomb_cool_down = 10
        Blue_body.length = 12*(3-1)+1

    def handle_events(event):
        if event in next_state[Blue_body.cur_direction]:
            if event == KED:
                if Blue_body.bomb_cool_down == 0:
                    bx, by = Blue_body.tx, Blue_body.ty
                    gw.addleft_object(Bomb(bx, by, Blue_body.length), 'bomb')
                    Blue_body.bomb_cool_down = 100
            else:
                Blue_body.direction.appendleft(event)
    
    def check_col(self):
        cur_loc = gw.field_array[self.gx+1][self.gy+1]
        if Blue_body.length >= 40 and \
            (cur_loc & (FIELD_DICT['body']+FIELD_DICT['head']) \
                == (FIELD_DICT['body']+FIELD_DICT['head'])):
            game_over()
        if cur_loc & (FIELD_DICT['wall']):
            game_over()
        if cur_loc & (FIELD_DICT['apple']):
            Blue_body.longer = True
        if cur_loc & (FIELD_DICT['poison']):
            Blue_body.get_damaged()

def game_over():
    import module_state.play_state as ps
    ps.isended = -1

GO_D, GO_W, GO_A, GO_S = range(4)

next_state = {
    GO_D: {KDD: GO_D, KWD: GO_W, KAD: GO_D, KSD: GO_S, KED: GO_D},
    GO_W: {KDD: GO_D, KWD: GO_W, KAD: GO_A, KSD: GO_W, KED: GO_W},
    GO_A: {KDD: GO_A, KWD: GO_W, KAD: GO_A, KSD: GO_S, KED: GO_A},
    GO_S: {KDD: GO_D, KWD: GO_S, KAD: GO_A, KSD: GO_S, KED: GO_S}
}