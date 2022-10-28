from pico2d import *
from random import *
from math import *
from coordinates_module import *
from collections import deque
from snake_move_images import *
from enemy_movement_ai import *

class enemy_body():
    def __init__(self, number, x=40, y=-1, color = 'orange'):
        if(y == -1):
            self.x, self.y = grid_to_coordinates(0, 8)
        else:
            self.x, self.y = x, y
        self.frame = 0
        self.number = number
        self.image = 0
        self.color = color
    def moves(self):
        global enemy_direction
        if(self.number == len(enemy_char) - 1):
            self.x, self.y = enemy_char[0].x + dx[enemy_direction], \
                enemy_char[0].y + dy[enemy_direction]
            self.number = 0
            enemy_char.rotate(1)
        else:
            if(self.number == 0):
                if(self.x % 60 == 40 and self.y % 60 == 40):
                    enemy_direction = enemy_order
            self.number += 1
        gx, gy = coordinates_to_grid(self.x, self.y)
        field_array[gx+1][gy+1] |= FIELD_DICT['enemy']

    def draw(self):
        if(self.number == 0):
            if(self.color == 'orange'):
                self.image = img_snake_orange_head[enemy_direction]
        else:
            if(self.color == 'orange'):
                self.image = img_snake_orange_body
        self.image.draw(self.x, self.y)

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
        field_array[gx+1][gy+1] |= FIELD_DICT['player']
        
    def draw(self):
        if(self.number == 0):
            self.image = img_snake_blue_head[cur_direction]
        else:
            self.image = img_snake_blue_body
        self.image.draw(self.x, self.y)

class explosion():
    def __init__(self, gx, gy, damage):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.image = img_explode
        self.frame = 6
        self.damage = damage
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
            explodes.appendleft(explosion(x, self.gy+1, self.damage))
        for x in range(self.gx+1, 16, +1):
            field_array[x][self.gy+1] |= 64
            explodes.appendleft(explosion(x, self.gy+1, self.damage))
        for y in range(self.gy+1, 10, +1):
            field_array[self.gx+1][y] |= 64
            explodes.appendleft(explosion(self.gx+1, y, self.damage))
        for y in range(self.gy+1, 0, -1):
            field_array[self.gx+1][y] |= 64
            explodes.appendleft(explosion(self.gx+1, y, self.damage))
        self.x = -65535
    def draw(self):
        cnt = ceil(self.counter / 70)
        if(self.counter > 0):
            global frame
            self.image = img_bomb[cnt - 1]
            self.image.clip_draw(0 + 60 * (frame % 3), 0, 60, 60, self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['bomb']
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
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['apple']
        else: return

def handle_events():
    global acting, direction, bomb_cool_down, next_module
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            acting = False
            next_module = ''
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                acting = False
                next_module = 'title'
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
    for snakes in (char_blue, enemy_char):
        le = len(snakes)
        for i in range(le):
            snakes[i].moves()
        for i in range(le-1, -1, -1):
            snakes[i].draw()

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
    for snakes in (char_blue, enemy_char):
        x, y = snakes[0].x, snakes[0].y
        gx, gy = coordinates_to_grid(x, y)
        bomb_touched = None
        if(field_array[gx+1][gy+1] & (FIELD_DICT['bomb'])):
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
    for snakes in (char_blue, enemy_char):
        gx, gy = coordinates_to_grid(snakes[0].x, snakes[0].y)
        if(field_array[gx+1][gy+1] & (FIELD_DICT['apple'])):
            field_array[gx+1][gy+1] &= (MAX_BITS - FIELD_DICT['apple'])
            if(length < 109 and snakes == char_blue):
                for i in range(length, length + 12):
                    char_blue.append(blue_body(i, char_blue[length-1].x, char_blue[length-1].y))
                length += 12
            del(apples)
            create_new_apple()

def enemy_set_bomb():
    global bomb_cool_down_enemy
    le = len(enemy_char)
    bx, by = enemy_char[le-1].x, enemy_char[le-1].y
    bombs.appendleft(bomb(bx, by, 0))
    bomb_cool_down_enemy = 200

def check_collide():
    global length
    gx, gy = coordinates_to_grid(char_blue[0].x, char_blue[0].y)
    if(field_array[gx+1][gy+1] & FIELD_DICT['wall']):
        exit(1)
    if(field_array[gx+1][gy+1] & FIELD_DICT['enemy']):
        exit(1)
    if(length >= 28):
        for i in range(14, length):
            if(get_distance(char_blue[i].x, char_blue[i].y, char_blue[0].x, char_blue[0].y) <= 30):
                exit(1)

def check_touched_by_enemy():
    global length
    gx, gy = coordinates_to_grid(enemy_char[0].x, enemy_char[0].y)
    if(field_array[gx+1][gy+1] & FIELD_DICT['player']):
        length -= 12
        for _ in range(12):
            char_blue.pop()
        if(length <= 1):
            exit(1)

def check_explode():
    global length, apples, enemy_hp
    attacked = False
    apple_destroy = False
    enemy_damaged = 0
    for exploding in explodes:
        if(exploding.frame != 5):
            continue
        x, y = exploding.gx, exploding.gy
        if field_array[x][y] & (FIELD_DICT['player']):
            attacked = True
        if field_array[x][y] & ( FIELD_DICT['apple']):
            apple_destroy = True
        if field_array[x][y] & ( FIELD_DICT['enemy']):
            enemy_damaged = exploding.damage \
                if (exploding.damage > enemy_damaged) else enemy_damaged

    if(apple_destroy):
        del(apples)
        create_new_apple()
    if(attacked):
        length -= 12
        for _ in range(12):
            char_blue.pop()
        if(length <= 1):
            exit(1)
    enemy_hp -= enemy_damaged
    if(enemy_hp <= 0):
        exit(2)

def enemy_hp_bar_draw():
    img_hpbar.clip_draw(0, 0, 40, 40, 460, 590, enemy_hp//2, 40)

def enters():
    global acting, frame, direction, cur_direction, field_array, \
        bomb_cool_down, next_module, length, bomb_cool_down_enemy
    global char_blue, apples, bombs, explodes, enemy_char, enemy_direction, \
        enemy_hp, enemy_order
    acting = True
    frame = 0
    direction = 0 #0:D, 1:W, 2:A, 3:S
    cur_direction = 0
    field_array = []
    bomb_cool_down = 0
    next_module = ''
    length = 12*(3-1)+1
    char_blue = deque([blue_body(i) for i in range(0, length)])
    apples = apple(10, 0)
    bombs = deque()
    explodes = deque()
    enemy_char = deque([enemy_body(i) for i in range(0, 12*(6-1)+1)])
    enemy_direction = 0
    enemy_order = 0
    bomb_cool_down_enemy = 500
    enemy_hp = 500

def exits():
    global acting, frame, direction, cur_direction, field_array, \
        bomb_cool_down, next_module, length, bomb_cool_down_enemy
    global char_blue, apples, bombs, explodes, enemy_char, enemy_direction,\
        enemy_order, enemy_hp
    acting = None
    frame = None
    direction = None #0:D, 1:W, 2:A, 3:S
    cur_direction = None
    enemy_direction = None
    field_array = None
    bomb_cool_down = None
    next_module = None
    length = None
    char_blue = None
    apples = None
    bombs = None
    explodes = None
    enemy_char = None
    enemy_order = None
    bomb_cool_down_enemy = None
    enemy_hp = None

def acts():
    global acting, field_array, apples, frame, bomb_cool_down, next_module
    global enemy_order, enemy_direction, enemy_char, bomb_cool_down_enemy
    acting = True
    while(acting):
        clear_canvas()
        field_array = field_array_reset()
        img_field.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        apples.draw()
        if bomb_cool_down_enemy == 0: enemy_set_bomb()
        bomb_count_and_draw()
        snake_move_and_draw()
        bomb_and_explode_delete()
        check_eat()
        check_eat_bomb()
        check_collide()
        check_explode()
        check_touched_by_enemy()
        explode_draw()
        enemy_hp_bar_draw()
        enemy_order = enemy_ai(enemy_direction, \
            *coordinates_to_grid(enemy_char[0].x, enemy_char[0].y), field_array, 2)
        update_canvas()
        handle_events()
        if bomb_cool_down > 0: bomb_cool_down -= 1
        if bomb_cool_down_enemy > 0: bomb_cool_down_enemy -= 1
        frame = (frame + 1) % 8
        delay(0.01)
    return next_module

acting = None
frame = None
direction = None #0:D, 1:W, 2:A, 3:S
cur_direction = None
field_array = None
bomb_cool_down = None
next_module = None
length = None
char_blue = None
apples = None
bombs = None
explodes = None
enemy_char = None
enemy_direction = None
enemy_order = None
bomb_cool_down_enemy = None
enemy_hp = None