from gettext import find
from pico2d import *
from random import *
from math import *
from numpy import *

UI_WIDTH, UI_HEIGHT = 920, 640
open_canvas(UI_WIDTH, UI_HEIGHT)

img_field = load_image('img/field.png')
img_snake_blue_head = \
    [load_image('img/snake_blue_head_' + str(i) + '.png') for i in range(4)]
img_snake_blue_body = load_image('img/snake_blue_body.png')
img_apple = load_image('img/apple.png')

acting = True
frame = 0
direction = 0 #0:D, 1:W, 2:A, 3:S
cur_direction = 0
snake_speed = 5
dx = [snake_speed, 0, -snake_speed, 0, 0]
dy = [0, +snake_speed, 0, -snake_speed, 0]

def field_array_reset():
    global field_array
    field_array = [[16] * 11]
    for i in range(0, 15):
        field_array += [[16] + [0] * 9 + [16]]
    field_array += [[16] * 11]

field_dict = {'empty': 0, 'player': 1, 'enemy':2, 'apple':4, \
    'bomb':8, 'wall':16, 'head':32}
field_array = [] #0:empty, 1:player, 2:enemy, 4:apple, 8:bomb, 16:wall, 32:head
field_array_reset()

def convert_coordinates(x, y):
    return x, UI_HEIGHT - y

def grid_to_coordinates(x, y):
    return (x * 60 + 40), UI_HEIGHT - (y * 60 + 120)

def coordinates_to_grid(x, y):
    return (x - 40) // 60, (-y + UI_HEIGHT - 120) // 60

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
            new_head = char_blue.pop()
            char_blue.insert(0, new_head)
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
char_blue = [blue_body(i) for i in range(0, length)]
appl = apple(randint(0, 14), randint(0, 8))

def handle_events():
    global acting, direction
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            acting = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            acting = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w and cur_direction not in (1,3):
            direction = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a and cur_direction not in (0,2):
            direction = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s and cur_direction not in (1,3):
            direction = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d and cur_direction not in (0,2):
            direction = 0

def snake_move_and_draw():
    for i in range(len(char_blue)):
        char_blue[i].moves()
    for i in range(len(char_blue)-1, -1, -1):
        char_blue[i].draw()

def check_eat():
    global length, appl
    gx, gy = coordinates_to_grid(char_blue[0].x, char_blue[0].y)
    if(field_array[gx+1][gy+1] & (field_dict['apple']+field_dict['player']) \
        == field_dict['apple'] + field_dict['player']):
        field_array[gx+1][gy+1] &= (65535- field_dict['apple'])
        if(length < 109):
            for i in range(length, length + 12):
                char_blue.append(blue_body(i, char_blue[length-1].x, char_blue[length-1].y))
            length += 12
        del(appl)
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
        appl = apple(new_apple_x, new_apple_y)

def get_distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def check_collide():
    global length, cur_direction
    gx, gy = coordinates_to_grid(char_blue[0].x, char_blue[0].y)
    if(field_array[gx+1][gy+1] & field_dict['wall']):
        exit(1)
    if(length >= 28):
        for i in range(14, length):
            if(get_distance(char_blue[i].x, char_blue[i].y, char_blue[0].x, char_blue[0].y) <= 30):
                exit(1)
        

while(acting):
    clear_canvas()
    field_array_reset()
    img_field.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    appl.draw()
    snake_move_and_draw()
    update_canvas()
    frame = (frame + 1) % 8
    #print(field_array)
    check_eat()
    check_collide()
    handle_events()
    delay(0.01)

close_canvas()
