from pico2d import *
from random import *
from math import *
from coordinates_module import *
from collections import deque
from snake_move_images import *

acting = True
frame = 0
direction = 0 #0:D, 1:W, 2:A, 3:S
cur_direction = 0
field_array = []
bomb_cool_down = 0

class blue_body():
    def __init__(self, number, x=40, y=-1):
        if(y == -1):
            self.x, self.y = convert_coordinates(x, 120)
        else:
            self.x, self.y = x, y
        self.frame = 0
        self.number = number
        self.image = 0
    def moves(self):
        global cur_direction
        if(self.number == len(char_blue) - 1):
            self.x, self.y = char_blue[0].x + dx[cur_direction], char_blue[0].y + dy[cur_direction]
            self.number = 0
            char_blue.rotate(1)
        else:
            if(self.number == 0):
                if(self.x % 60 == 40 and self.y % 60 == 40):
                    cur_direction = direction
            self.number += 1
        gx, gy = coordinates_to_grid(self.x, self.y)
        field_array[gx+1][gy+1] |= field_dict['player']
        
    def draw(self):
        if(self.number == 0):
            self.image = img_snake_blue_head[cur_direction]
        else:
            self.image = img_snake_blue_body
        self.image.draw(self.x, self.y)

class explosion():
    def __init__(self, gx, gy):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.image = img_explode
        self.frame = 6
    def draw(self):
        self.image.clip_draw(0 + 60 * (self.frame // 2), 0, 60, 60, self.x, self.y)

class bomb():
    def __init__(self, x, y, damage):
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        self.image = img_bomb[4]
        self.counter = 350
        self.damage = damage
    def explode(self):
        for x in range(self.gx+1, 0, -1):
            field_array[x][self.gy+1] |= 64
            explodes.appendleft(explosion(x, self.gy+1))
        for x in range(self.gx+1, 17, +1):
            field_array[x][self.gy+1] |= 64
            explodes.appendleft(explosion(x, self.gy+1))
        for y in range(self.gy+1, 11, +1):
            field_array[self.gx+1][y] |= 64
            explodes.appendleft(explosion(self.gx+1, y))
        for y in range(self.gy+1, 0, -1):
            field_array[self.gx+1][y] |= 64
            explodes.appendleft(explosion(self.gx+1, y))
        self.x = -65535
    def draw(self):
        cnt = ceil(self.counter / 70)
        if(self.counter > 0):
            global frame
            self.image = img_bomb[cnt - 1]
            self.image.clip_draw(0 + 60 * (frame % 3), 0, 60, 60, self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= field_dict['bomb']
        elif(self.counter == 0 or self.counter <= -65535):
            self.explode()
        else:
            return

class apple():
    def __init__(self, gx, gy):
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.image = img_apple
        self.exist = True
    def draw(self):
        if(self.exist):
            self.image.draw(self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= field_dict['apple']
        else: return

length = 12*(3-1)+1
char_blue = deque([blue_body(i) for i in range(0, length)])
apples = apple(randint(0, 14), randint(0, 8))
bombs = deque()
explodes = deque()

def handle_events():
    global acting, direction, bomb_cool_down
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            acting = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                acting = False
            elif event.key == SDLK_w and cur_direction not in (1,3):
                direction = 1
            elif event.key == SDLK_a and cur_direction not in (0,2):
                direction = 2
            elif event.key == SDLK_s and cur_direction not in (1,3):
                direction = 3
            elif event.key == SDLK_d and cur_direction not in (0,2):
                direction = 0
            elif event.key == SDLK_e and bomb_cool_down == 0:
                le = len(char_blue)
                bx, by = char_blue[le-1].x, char_blue[le-1].y
                bombs.appendleft(bomb(bx, by, length))
                bomb_cool_down = 100

def snake_move_and_draw():
    le = len(char_blue)
    for i in range(le):
        char_blue[i].moves()
    for i in range(le-1, -1, -1):
        char_blue[i].draw()

def bomb_count_and_draw():
    le = len(bombs)
    for i in range(le):
        bombs[i].draw()
    for i in range(le):
        bombs[i].counter -= 1
        
def bomb_and_explode_delete():
    le = len(bombs)
    for i in range(le-1, -1, -1):
        if(bombs[i].counter >= 0):
            break
        bombs.pop()
    le = len(explodes)
    for i in range(le-1, -1, -1):
        if(explodes[i].frame >= 0):
            break
        explodes.pop()

def explode_draw():
    le = len(explodes)
    for i in range(le):
        explodes[i].frame -= 1
    for i in range(le-1, -1, -1):
        explodes[i].draw()

def create_new_apple():
    global apples
    new_apple_x = 0
    new_apple_y = 0
    while(field_array[new_apple_x][new_apple_y] != 0 \
        or field_array[new_apple_x][new_apple_y-1] != 0 \
            or field_array[new_apple_x][new_apple_y+1] != 0 \
                or field_array[new_apple_x-1][new_apple_y] != 0 \
                    or field_array[new_apple_x-1][new_apple_y-1] != 0 \
                        or field_array[new_apple_x-1][new_apple_y+1] != 0 \
                            or field_array[new_apple_x+1][new_apple_y] != 0 \
                                or field_array[new_apple_x+1][new_apple_y-1] != 0 \
                                    or field_array[new_apple_x+1][new_apple_y+1] != 0):
        new_apple_x = randint(0, 14)
        new_apple_y = randint(0, 8)
    apples = apple(new_apple_x, new_apple_y)

def check_eat_bomb():
    global bombs
    x, y = char_blue[0].x, char_blue[0].y
    gx, gy = coordinates_to_grid(x, y)
    bomb_touched = None
    if(field_array[gx+1][gy+1] & (field_dict['bomb']+field_dict['player']) \
        == field_dict['bomb'] + field_dict['player']):
        for bo in bombs:
            if get_distance(x, y, bo.x, bo.y) < 20:
                bo.counter = -65535
                bomb_touched = bo
                break
        if bomb_touched != None:
            bombs.remove(bomb_touched)
            bombs.append(bomb_touched)


def check_eat():
    global length, apples
    gx, gy = coordinates_to_grid(char_blue[0].x, char_blue[0].y)
    if(field_array[gx+1][gy+1] & (field_dict['apple']+field_dict['player']) \
        == field_dict['apple'] + field_dict['player']):
        field_array[gx+1][gy+1] &= (65535- field_dict['apple'])
        if(length < 109):
            for i in range(length, length + 12):
                char_blue.append(blue_body(i, char_blue[length-1].x, char_blue[length-1].y))
            length += 12
        del(apples)
        create_new_apple()

def check_collide():
    global length, cur_direction
    gx, gy = coordinates_to_grid(char_blue[0].x, char_blue[0].y)
    if(field_array[gx+1][gy+1] & field_dict['wall']):
        exit(1)
    if(field_array[gx+1][gy+1] & field_dict['enemy']):
        exit(1)
    if(length >= 28):
        for i in range(14, length):
            if(get_distance(char_blue[i].x, char_blue[i].y, char_blue[0].x, char_blue[0].y) <= 30):
                exit(1)

def check_explode():
    global length, apples
    attacked = False
    apple_destroy = False
    for x in range(1, 16):
        for y in range(1, 10):
            if field_array[x][y] & (field_dict['explode'] + field_dict['player']) == \
                field_dict['explode'] + field_dict['player']:
                attacked = True
            if field_array[x][y] & (field_dict['explode'] + field_dict['apple']) == \
                field_dict['explode'] + field_dict['apple']:
                apple_destroy = True
            if(apple_destroy and attacked): break
        if(apple_destroy and attacked): break
    if(apple_destroy):
        del(apples)
        create_new_apple()
    if(attacked):
        length -= 12
        for _ in range(12):
            char_blue.pop()
        if(length <= 1):
            exit(1)        

while(acting):
    clear_canvas()
    field_array = field_array_reset()
    img_field.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    apples.draw()
    img_snake_orange_head[0].draw(*grid_to_coordinates(0,8))
    field_array[1][9] |= field_dict['enemy']
    bomb_count_and_draw()
    snake_move_and_draw()
    bomb_and_explode_delete()
    check_eat()
    check_eat_bomb()
    check_collide()
    check_explode()
    explode_draw()
    update_canvas()
    handle_events()
    if bomb_cool_down > 0: bomb_cool_down -= 1
    frame = (frame + 1) % 8
    delay(0.01)

close_canvas()
