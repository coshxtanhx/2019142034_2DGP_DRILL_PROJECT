from coordinates_module import *
from collections import deque
from pico2d import *
from event_table_module import *
from module_object.bomb_obj import bomb

class Blue_body():
    img_snake_blue_head = None
    img_snake_blue_body = None
    cur_direction = 0
    # direction = 0
    direction = deque(maxlen=4)
    bomb_cool_down = 10
    length = 12*(3-1)+1
    def __init__(self, number, x=40, y=-1):
        if(y == -1):
            self.x, self.y = convert_coordinates(x, 120)
        else:
            self.x, self.y = x, y
        self.frame = 0
        self.number = number
        self.image = 0
        if(Blue_body.img_snake_blue_head == None):
            Blue_body.img_snake_blue_head = \
                [load_image('img/snake_blue_head_' + str(i) + '.png')\
                    for i in range(4)]
            Blue_body.img_snake_blue_body = load_image('img/snake_blue_body.png')
    def moves(self, char_blue, field_array):
        if(self.number == len(char_blue) - 1):
            self.x, self.y = char_blue[0].x + dx[Blue_body.cur_direction], \
                char_blue[0].y + dy[Blue_body.cur_direction]
            self.number = 0
            char_blue.rotate(1)
        else:
            if(self.number == 0):
                if(Blue_body.direction and self.x % 60 == 40 and self.y % 60 == 40):
                    Blue_body.cur_direction = \
                        next_state[Blue_body.cur_direction][Blue_body.direction.pop()]
            self.number += 1
        gx, gy = coordinates_to_grid(self.x, self.y)
        field_array[gx+1][gy+1] |= FIELD_DICT['player']
        
    def draw(self):
        if(self.number == 0):
            self.image = Blue_body.img_snake_blue_head[self.cur_direction]
        else:
            self.image = Blue_body.img_snake_blue_body
        self.image.draw(self.x, self.y)
    def reset():
        Blue_body.cur_direction = 0
        Blue_body.direction = deque(maxlen=2)
        Blue_body.bomb_cool_down = 10
        Blue_body.length = 12*(3-1)+1

    def handle_events(event, tail, bombs):
        print(Blue_body.direction)
        if event in next_state[Blue_body.cur_direction]:
            if event == KED:
                if Blue_body.bomb_cool_down == 0:
                    bx, by = tail.x, tail.y
                    bombs.appendleft(bomb(bx, by, Blue_body.length))
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