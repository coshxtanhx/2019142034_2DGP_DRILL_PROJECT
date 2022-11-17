from pico2d import *
from random import *
from math import *
from module_other.coordinates_module import *
from module_other.event_table_module import *
from collections import deque
from module_object.apple_obj import *
from module_object.bomb_obj import *
from module_object.mine_obj import *
from module_object.snake_player_obj import *
from module_object.snake_enemy_obj import *
from module_object.hpbar_obj import *
from module_object.screen_hider_obj import *
from module_object.background_obj import *
import module_other.state_changer
import module_other.game_world
from pprint import pprint

def handle_events():
    Enemy_body.enemy_set_bomb()
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            module_other.state_changer.change_state('', None)
        elif event == KESCD:
            module_other.state_changer.change_state('title', None)
        else:
            Blue_body.handle_events(event)
        if raw_event.key == SDLK_p: Enemy_body.enemy_hp -= 125
        elif raw_event.key == SDLK_l: Enemy_body.armored.append(randint(0,5)*12)
        elif event == KMD:
            module_other.state_changer.change_state('game_menu', 'pause')

def enters(data):
    global frame, field_array
    global char_blue, apples, bombs, explodes, enemy_char
    global enemy_hpbar, broken_screen, screen_out, cloud, ices, mine
    global cur_char, cur_stage
    if(data == None): data = '11'
    cur_char, cur_stage = data[0], data[1]
    frame = 0
    field_array = field_array_reset()

    Blue_body.character = cur_char

    module_other.game_world.add_object(Background('play'), 'bg')
    module_other.game_world.add_objects([Blue_body(i) for i in range(12*(3-1)+1)], 'player')
    module_other.game_world.addleft_object(create_first_apple(), 'obj')
    module_other.game_world.add_objects([Enemy_body(i, color=COLOR_DICT[cur_stage]) \
        for i in range(0, 12*(6-1)+1)], 'enemy')
    module_other.game_world.add_object(HP_bar(int(cur_stage)-1), 'ui')
    for snake in (Blue_body, Enemy_body):
        snake.reset()

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
    module_other.game_world.clear_world()

def draw_all():
    global field_array, apples, frame
    global enemy_char
    clear_canvas()
    module_other.game_world.field_array = field_array_reset()
    for objs in module_other.game_world.all_objects():
        objs.draw()
    update_canvas()
    # pprint(game_world.field_array)

def update():
    for objs in module_other.game_world.all_objects_copy():
        objs.update()
    module_other.game_world.rotate_object(1, 'player')
    module_other.game_world.rotate_object(1, 'enemy')

    for objs in module_other.game_world.all_objects_copy():
        objs.check_col()

    Blue_body.get_longer()
    Blue_body.get_shorter()

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