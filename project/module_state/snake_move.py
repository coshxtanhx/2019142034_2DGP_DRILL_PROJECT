from pico2d import *
from random import *
from math import *
from coordinates_module import *
from event_table_module import *
from collections import deque
from snake_move_images import *
from enemy_movement_ai import *
from module_object.apple_obj import *
from module_object.bomb_obj import *
from module_object.snake_player_obj import *
from module_object.snake_enemy_obj import *
from module_object.hpbar_obj import *
from module_object.screen_hider_obj import *

def handle_events():
    global acting, next_module, next_module_option
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            acting = False
            next_module, next_module_option = '', None
        elif event == KESCD:
            acting = False
            next_module, next_module_option = '', None
        elif event == KWD and Blue_body.cur_direction not in (1,3):
            Blue_body.direction = 1
        elif event == KAD and Blue_body.cur_direction not in (0,2):
            Blue_body.direction = 2
        elif event == KSD and Blue_body.cur_direction not in (1,3):
            Blue_body.direction = 3
        elif event == KDD and Blue_body.cur_direction not in (0,2):
            Blue_body.direction = 0
        elif event == KED and Blue_body.bomb_cool_down == 0:
            le = len(char_blue)
            bx, by = char_blue[le-1].x, char_blue[le-1].y
            bombs.appendleft(bomb(bx, by, Blue_body.length))
            Blue_body.bomb_cool_down = 100
        global zzz
        if raw_event.key == SDLK_u: zzz = 0
        elif raw_event.key == SDLK_i: zzz = 1
        elif raw_event.key == SDLK_o: zzz = 2
        elif raw_event.key == SDLK_p: zzz = 3
        elif event == KMD:
            acting = False
            next_module, next_module_option = 'game_menu', 'pause'

zzz = 1
def snake_move_and_draw():
    for snakes in (char_blue, enemy_char):
        le = len(snakes)
        for i in range(le):
            snakes[i].moves(snakes, field_array)
        for i in range(le-1, -1, -1):
            snakes[i].draw()

def bomb_count_and_draw():
    le = len(bombs)
    for i in range(le):
        bombs[i].draw(field_array, explodes, ices, frame)
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
    le = len(ices)
    for i in range(le-1, -1, -1):
        if(ices[i].frame < 0):
            del ices[i]

def explode_draw():
    le = len(explodes)
    for i in range(le):
        explodes[i].frame -= 1
    for i in range(le-1, -1, -1):
        explodes[i].draw()
    le = len(ices)
    for i in range(le):
        ices[i].frame -= 1
    for i in range(le-1, -1, -1):
        ices[i].draw(field_array)

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
    global apples
    ap_loc = field_array[apples.gx+1][apples.gy+1]
    eaten = False

    if(ap_loc & FIELD_DICT['player']):
        eaten = True
        if(Blue_body.length < 109):
            for i in range(Blue_body.length, Blue_body.length + 12):
                char_blue.append(Blue_body(i, char_blue[Blue_body.length-1].x, \
                    char_blue[Blue_body.length-1].y))
            Blue_body.length += 12
    elif(ap_loc & (FIELD_DICT['enemy'])):
        eaten = True
    if(eaten):
        del(apples)
        create_new_apple()

def enemy_set_bomb():
    le = len(enemy_char)
    bx, by = enemy_char[le-1].x, enemy_char[le-1].y
    bombs.appendleft(bomb(bx, by, 0, randint(0, 3)))
    Enemy_body.bomb_cool_down = 200

def check_collide():
    gx, gy = coordinates_to_grid(char_blue[0].x, char_blue[0].y)
    if(field_array[gx+1][gy+1] & FIELD_DICT['wall']):
        exit(1)
    if(field_array[gx+1][gy+1] & (FIELD_DICT['enemy'])):
        exit(1)
    if(Blue_body.length >= 28):
        for i in range(14, Blue_body.length):
            if(get_distance(char_blue[i].x, char_blue[i].y,
                char_blue[0].x, char_blue[0].y) <= 30):
                exit(1)

def check_touched_by_enemy():
    gx, gy = coordinates_to_grid(enemy_char[0].x, enemy_char[0].y)
    if(field_array[gx+1][gy+1] & FIELD_DICT['player']):
        Blue_body.length -= 12
        for _ in range(12):
            char_blue.pop()
        if(Blue_body.length <= 1):
            exit(1)

def check_attacked_by_ices():
    global ices
    ice_removing_obj = FIELD_DICT['enemy'] + FIELD_DICT['explode'] \
        + FIELD_DICT['bomb'] + FIELD_DICT['apple']
    remove_ice = []
    player_attacked = False
    for ice in ices:
        gx, gy = coordinates_to_grid(ice.x, ice.y)
        if(not(player_attacked) and \
            (field_array[gx+1][gy+1] & FIELD_DICT['player'])):
            remove_ice.append(ice)
            player_attacked = True
        if(field_array[gx+1][gy+1] & ice_removing_obj):
            remove_ice.append(ice)
    if(player_attacked):
        Blue_body.length -= 12
        for _ in range(12):
            char_blue.pop()
        if(Blue_body.length <= 1):
            exit(1)
    for ice in remove_ice:
        ices.remove(ice)

def check_explode():
    global apples
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
        if field_array[x][y] & FIELD_DICT['enemy']:
            enemy_damaged = exploding.damage \
                if (exploding.damage > enemy_damaged) else enemy_damaged

    if(apple_destroy):
        del(apples)
        create_new_apple()
    if(attacked):
        Blue_body.length -= 12
        for _ in range(12):
            char_blue.pop()
        if(Blue_body.length <= 1):
            exit(1)
    Enemy_body.enemy_hp -= enemy_damaged
    if(Enemy_body.enemy_hp <= 0):
        print('victory')
        exit(2)

def screen_hider_draw():
    return
    global cloud
    if(cloud.x < -170):
        cloud = Cloud()
    cloud.draw()
    for i in broken_screen:
        i.draw()
    screen_out.draw(char_blue[0].x, char_blue[0].y)

def enemy_hp_bar_draw():
    enemy_hpbar.draw(Enemy_body.enemy_hp)

def enters(option):
    global acting, frame, field_array, next_module, next_module_option
    global char_blue, apples, bombs, explodes, enemy_char
    global enemy_hpbar, broken_screen, screen_out, cloud, ices
    global cur_char, cur_stage
    cur_char, cur_stage = option[0], option[1]
    acting = True
    frame = 0
    field_array = []
    next_module = ''
    next_module_option = ''
    char_blue = deque([Blue_body(i) for i in range(0, 12*(3-1)+1)])
    apples = apple(10, 0)
    bombs = deque()
    explodes = deque()
    enemy_char = deque([Enemy_body(i, color=COLOR_DICT[cur_stage]) \
        for i in range(0, 12*(6-1)+1)])
    for snake in (Blue_body, Enemy_body):
        snake.reset()
    enemy_hpbar = HP_bar(int(option[1])-1)
    broken_screen = [Broken() for _ in range(4)]
    screen_out = Screen_off()
    cloud = Cloud()
    ices = []

def exits():
    global acting, frame, field_array, next_module, next_module_option
    global char_blue, apples, bombs, explodes, enemy_char
    global enemy_hpbar, broken_screen, screen_out, cloud, ices
    global cur_char, cur_stage
    acting = None
    frame = None
    field_array = None
    next_module = None
    next_module_option = None
    char_blue = None
    apples = None
    bombs = None
    explodes = None
    enemy_char = None
    enemy_hpbar = None
    broken_screen = None
    screen_out = None
    cloud = None
    ices = None
    cur_char = None
    cur_stage = None

def acts():
    global acting, field_array, apples, frame, next_module
    global enemy_char
    acting = True
    while(acting):
        clear_canvas()
        field_array = field_array_reset()
        img_field.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        apples.draw(field_array)
        if Enemy_body.bomb_cool_down == 0: enemy_set_bomb()
        bomb_count_and_draw()
        snake_move_and_draw()
        bomb_and_explode_delete()
        check_eat()
        check_eat_bomb()
        check_collide()
        check_explode()
        check_attacked_by_ices()
        check_touched_by_enemy()
        explode_draw()
        screen_hider_draw()
        enemy_hp_bar_draw()
        Enemy_body.enemy_order = enemy_ai(Enemy_body.enemy_direction, \
            *coordinates_to_grid(enemy_char[0].x, enemy_char[0].y), field_array, zzz)
        update_canvas()
        handle_events()
        for snake in (Blue_body, Enemy_body):
            if snake.bomb_cool_down > 0: snake.bomb_cool_down -= 1
        frame = (frame + 1) % 8
        delay(0.01)
    return next_module, next_module_option

acting = None
frame = None
field_array = None
next_module = None
next_module_option = None
char_blue = None
apples = None
bombs = None
explodes = None
enemy_char = None
enemy_hpbar = None
broken_screen = None
screen_out = None
cloud = None
ices = None
cur_char = None
cur_stage = None