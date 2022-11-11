from pico2d import *
from random import *
from math import *
from coordinates_module import *
from event_table_module import *
from collections import deque
from snake_move_images import *
from module_object.apple_obj import *
from module_object.bomb_obj import *
from module_object.mine_obj import *
from module_object.snake_player_obj import *
from module_object.snake_enemy_obj import *
from module_object.hpbar_obj import *
from module_object.screen_hider_obj import *
from module_object.background_obj import *
import state_changer

def game_over():
    state_changer.change_state('title_menu', None)

def go_next_stage():
    next_stage = str(int(cur_stage) + 1)
    if next_stage == '5':
        all_clear()
    state_changer.change_state('snake_move', 'exitall', cur_char + next_stage)

def all_clear():
    exit(2)

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            state_changer.change_state('', None)
        elif event == KESCD:
            state_changer.change_state('title', None)
        else:
            Blue_body.handle_events(event, char_blue[-1], bombs)
        global zzz
        if raw_event.key == SDLK_u: Enemy_body.ai = 0
        elif raw_event.key == SDLK_i: Enemy_body.ai = 5
        elif raw_event.key == SDLK_o: Enemy_body.ai = 4
        elif raw_event.key == SDLK_p: Enemy_body.ai = 3
        elif raw_event.key == SDLK_l: Enemy_body.armored.append(randint(0,5)*12)
        elif event == KMD:
            state_changer.change_state('game_menu', 'pause')

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
        if(apples.poisoned == False and Blue_body.length < 109):
            for i in range(Blue_body.length, Blue_body.length + 12):
                char_blue.append(Blue_body(i, char_blue[Blue_body.length-1].x, \
                    char_blue[Blue_body.length-1].y))
            Blue_body.length += 12
        elif(apples.poisoned):
            if(Blue_body.length < 15):
                game_over()
            else:
                Blue_body.length -= 12
                for _ in range(12):
                    char_blue.pop()

    elif(ap_loc & (FIELD_DICT['enemy'])):
        eaten = True
    if(eaten):
        del(apples)
        apples = create_new_apple(field_array, cur_char)

def enemy_set_bomb():
    le = len(enemy_char)
    bx, by = enemy_char[le-1].x, enemy_char[le-1].y
    bombs.appendleft(bomb(bx, by, 0, randint(0, 0)))
    Enemy_body.bomb_cool_down = 200

def check_collide():
    gx, gy = coordinates_to_grid(char_blue[0].x, char_blue[0].y)
    if(field_array[gx+1][gy+1] & (FIELD_DICT['enemy'] + FIELD_DICT['wall'])):
        game_over()
    if(Blue_body.length >= 28):
        for i in range(14, Blue_body.length):
            if(get_distance(char_blue[i].x, char_blue[i].y,
                char_blue[0].x, char_blue[0].y) <= 30):
                game_over()

def check_touched_by_enemy():
    gx, gy = coordinates_to_grid(enemy_char[0].x, enemy_char[0].y)
    if(field_array[gx+1][gy+1] & FIELD_DICT['player']):
        Blue_body.length -= 12
        for _ in range(12):
            char_blue.pop()
        if(Blue_body.length <= 1):
            game_over()

def check_attacked_by_ices():
    global ices
    ice_removing_obj = FIELD_DICT['enemy'] + FIELD_DICT['explode'] \
        + FIELD_DICT['bomb'] + FIELD_DICT['apple']
    remove_ice = []
    player_attacked = False
    for ice in ices:
        gx, gy = coordinates_to_grid(ice.x, ice.y)
        if(field_array[gx+1][gy+1] & FIELD_DICT['player']):
            field_array[gx+1][gy+1] &= MAX_BITS - FIELD_DICT['ice']
            remove_ice.append(ice)
            player_attacked = True
        elif(field_array[gx+1][gy+1] & ice_removing_obj):
            remove_ice.append(ice)
    for ice in remove_ice:
        ices.remove(ice)
    if(player_attacked):
        Blue_body.length -= 12
        for _ in range(12):
            char_blue.pop()
        if(Blue_body.length <= 1):
            game_over()

def check_explode():
    global apples
    attacked = False
    apple_destroy = False
    enemy_damaged = 0
    armor_not_touched = True
    for exploding in explodes:
        if(exploding.frame != 5):
            continue
        x, y = exploding.gx, exploding.gy
        if field_array[x][y] & (FIELD_DICT['player']):
            attacked = True
        if field_array[x][y] & (FIELD_DICT['poison'] + FIELD_DICT['apple']):
            apple_destroy = True
        if field_array[x][y] & ( FIELD_DICT['armor']):
            armor_not_touched = False
        if armor_not_touched and (field_array[x][y] & FIELD_DICT['enemy']):
            enemy_damaged = exploding.damage \
                if (exploding.damage > enemy_damaged) else enemy_damaged

    if(apple_destroy):
        del(apples)
        apples = create_new_apple(field_array, cur_char)
    if(attacked):
        Blue_body.length -= 12
        for _ in range(12):
            char_blue.pop()
        if(Blue_body.length <= 1):
            game_over()
    Enemy_body.enemy_hp -= enemy_damaged
    if(Enemy_body.enemy_hp <= 0):
        Enemy_body.enemy_hp = 0
        print('victory')
        go_next_stage()

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

def check_interaction():
    check_eat()
    check_eat_bomb()
    check_collide()
    check_explode()
    check_attacked_by_ices()
    check_touched_by_enemy()

def enters(data):
    global frame, field_array
    global char_blue, apples, bombs, explodes, enemy_char
    global enemy_hpbar, broken_screen, screen_out, cloud, ices, mine
    global cur_char, cur_stage
    if(data == None): data = '11'
    cur_char, cur_stage = data[0], data[1]
    frame = 0
    field_array = field_array_reset()
    char_blue = deque([Blue_body(i) for i in range(0, 12*(3-1)+1)])
    apples = create_first_apple(field_array, cur_char)
    bombs = deque()
    explodes = deque()
    enemy_char = deque([Enemy_body(i, color=COLOR_DICT[cur_stage]) \
        for i in range(0, 12*(6-1)+1)])
    for snake in (Blue_body, Enemy_body):
        snake.reset()
    enemy_hpbar = HP_bar(int(cur_stage)-1)
    broken_screen = [Broken() for _ in range(4)]
    screen_out = Screen_off()
    cloud = Cloud()
    ices = []
    mine = Mine(field_array)

def exits():
    global frame, field_array
    global char_blue, apples, bombs, explodes, enemy_char
    global enemy_hpbar, broken_screen, screen_out, cloud, ices
    global cur_char, cur_stage
    frame = None
    field_array = None
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

def draw_all():
    global field_array, apples, frame
    global enemy_char
    clear_canvas()
    field_array = field_array_reset()
    img_field.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    apples.draw(field_array)
    if Enemy_body.bomb_cool_down == 0: enemy_set_bomb()
    mine.draw(field_array)
    bomb_count_and_draw()
    snake_move_and_draw()
    explode_draw()
    screen_hider_draw()
    enemy_hp_bar_draw()
    update_canvas()

def update():
    global field_array, apples, frame
    global enemy_char
    bomb_and_explode_delete()
    check_interaction()
    mine.is_snake_here(field_array)
    for snake in (Blue_body, Enemy_body):
        if snake.bomb_cool_down > 0: snake.bomb_cool_down -= 1
    Enemy_body.enemy_ai_update(enemy_char[0], field_array)
    frame = (frame + 1) % 8

frame = None
field_array = None
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
mine = None
cur_char = None
cur_stage = None