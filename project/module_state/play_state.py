from pico2d import *
from random import *
from math import *
from module_other.coordinates_module import *
from module_other.event_table_module import *
from module_object.apple import *
from module_object.bomb import *
from module_object.mine import *
import module_object.snake_player as sp
import module_object.snake_enemy as se
from module_object.ui.hpbar import *
from module_object.screen_hider import *
from module_object.ui.background import *
import module_other.state_changer as sc
import module_other.game_world as gw
import module_other.bgm_player as bp
from pprint import pprint

def is_game_ended():
    if isended == DEFEAT:
        sc.change_state('game_over', None, cur_char + cur_stage)
    elif isended == VICTORY:
        next_stage = str(int(cur_stage) + 1)
        length = str(sp.Blue_body.length // 12 - 1) 
        sc.change_state('game_clear', 'exitall', cur_char + next_stage + length)
    else:
        return

def handle_events():
    if cur_stage == '5':
        sc.change_state('ending', None)
        return
    se.Enemy_body.enemy_set_bomb()
    se.Enemy_body.enemy_screen_off()
    se.Enemy_body.create_cloud()
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            sc.change_state('', None)
        elif event == KESCD:
            sc.change_state('game_menu', 'pause')
        else:
            sp.Blue_body.handle_events(event)
        if raw_event.key == SDLK_p: se.Enemy_body.damaged = 125

def enters(data):
    global frame, field_array, isended
    global cur_char, cur_stage
    if(data == None): data = GENERAL_SNAKE + STAGE1
    cur_char, cur_stage = data[0], data[1]

    if data[1] == ENDING:
        return

    frame = 0
    field_array = field_array_reset()
    isended = STILL_PLAYING

    sp.Blue_body.character = cur_char

    for snake in (sp.Blue_body, se.Enemy_body):
        snake.reset()

    gw.add_object(Background('play'), 'bg')
    gw.add_objects([sp.Blue_body(i) for i in range(12*(3-1)+1)], 'player')
    gw.addleft_object(create_first_apple(), 'obj')
    gw.add_objects([se.Enemy_body(i, color=se.COLOR_DICT[cur_stage]) \
        for i in range(0, 12*(6-1)+1)], 'enemy')
    gw.add_object(HP_bar(int(cur_stage)-1), 'ui')

    bp.bgm = bp.Stage_bgm(cur_stage)

def exits():
    global frame, field_array, isended
    global cur_char, cur_stage
    for snake in (sp.Blue_body, se.Enemy_body):
        snake.reset()
    frame = None
    field_array = None
    cur_char = None
    cur_stage = None
    isended = None
    gw.clear_world()

def draw_all():
    if cur_stage == '5':
        sc.change_state('ending', None)
        return

    global field_array, frame
    clear_canvas()
    gw.field_array = field_array_reset()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()
    # pprint(game_world.field_array)

def update():
    if cur_stage == '5':
        sc.change_state('ending', None)
        return
    for objs in gw.all_objects_copy():
        objs.update()
    gw.rotate_object(1, 'player')
    gw.rotate_object(1, 'enemy')

    for objs in gw.all_collision_objects():
        objs.check_col()

    sp.Blue_body.get_longer()
    sp.Blue_body.get_shorter()

    is_game_ended()

frame = None
field_array = None
cur_char = None
cur_stage = None
isended = None