from coordinates_module import *
from collections import deque
from pico2d import *
from event_table_module import *
from module_object.bomb_obj import bomb
import game_world

class Blue_body():
    img_snake_blue_head = None
    img_snake_blue_body = None
    cur_direction = 0
    # direction = 0
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
        else:
            if(self.number == 0):
                if(Blue_body.direction and self.x % 60 == 40 and self.y % 60 == 40):
                    Blue_body.cur_direction = \
                        next_state[Blue_body.cur_direction][Blue_body.direction.pop()]
            self.number += 1
        
    def draw(self):
        self.gx, self.gy = coordinates_to_grid(self.x, self.y)
        if(self.number == 0):
            game_world.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['head']
            Blue_body.hx, Blue_body.hy = self.x, self.y
            return
        else:
            self.image = Blue_body.img_snake_blue_body
            if(self.number == self.length-1):
                Blue_body.tx, Blue_body.ty = self.x, self.y
        self.image.draw(self.x, self.y)
        game_world.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['player']
        if(self.number == self.length - 1):
            (Blue_body.img_snake_blue_head[Blue_body.cur_direction]\
                ).draw(Blue_body.hx, Blue_body.hy)

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
                    game_world.addleft_object(bomb(bx, by, Blue_body.length), 'bomb')
                    Blue_body.bomb_cool_down = 100
            else:
                Blue_body.direction.appendleft(event)

GO_D, GO_W, GO_A, GO_S = range(4)

next_state = {
    GO_D: {KDD: GO_D, KWD: GO_W, KAD: GO_D, KSD: GO_S, KED: GO_D},
    GO_W: {KDD: GO_D, KWD: GO_W, KAD: GO_A, KSD: GO_W, KED: GO_W},
    GO_A: {KDD: GO_A, KWD: GO_W, KAD: GO_A, KSD: GO_S, KED: GO_A},
    GO_S: {KDD: GO_D, KWD: GO_S, KAD: GO_A, KSD: GO_S, KED: GO_S}
}