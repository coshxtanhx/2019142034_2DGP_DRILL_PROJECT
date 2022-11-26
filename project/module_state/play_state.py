from pico2d import *
from random import *
from math import *
from module_other.coordinates_module import *
from module_other.event_table_module import *
from module_object.apple import *
from module_object.bomb import *
from module_object.mine import *
from module_object.skin_wall import *
import module_object.snake_player as sp
import module_object.snake_enemy as se
from module_object.ui.hpbar import *
from module_object.screen_hider import *
from module_object.ui.background import *
import module_other.game_framework as gf
import module_other.game_world as gw
import module_other.sound_manager as sm
import module_other.collision_manager as cm
import module_other.server as sv
from pprint import pprint

def is_game_ended():
    if isended == DEFEAT:
        gf.change_state('game_over', None, cur_char + cur_stage)
    elif isended == VICTORY:
        next_stage = str(int(cur_stage) + 1)
        length = str(sp.Player_body.length // 12 - 1) 
        gf.change_state('game_clear', 'exitall', cur_char + next_stage + length)
    return

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            gf.change_state('', None)
        elif event == KESCD:
            gf.change_state('game_menu', 'pause')
        else:
            sv.player.handle_events(event)
        if raw_event.key == SDLK_p: se.Enemy_body.damaged = 125

def enter(data):
    global frame, field_array, isended
    global cur_char, cur_stage
    if(data == None): data = (GENERAL_SNAKE, STAGE1)
    cur_char, cur_stage = data[0], data[1]

    if data[1] == ENDING:
        gf.change_state('ending', None)
        return

    frame = 0
    field_array = field_array_reset()
    isended = STILL_PLAYING
    for snake in (se.Enemy_body,):
        snake.reset()

    sv.bg = Background('play')
    sv.player = sp.Player(cur_char)
    sv.apple = create_first_apple()
    sv.enemy = [se.Enemy_body(i, color=se.COLOR_DICT[cur_stage]) \
        for i in range(0, 12*(6-1)+1)]
    sv.hp_bar = HP_bar(int(cur_stage)-1)

    gw.add_object(sv.bg, 'bg')
    gw.add_object(sv.player, 'player')
    gw.add_object(sp.pHead(), 'player')
    gw.addleft_object(sv.apple, 'obj')
    gw.add_objects(sv.enemy, 'enemy')
    gw.add_object(sv.hp_bar, 'ui')
    sm.bgm = sm.Stage_bgm(cur_stage)

def exit():
    global frame, field_array, isended
    global cur_char, cur_stage
    for snake in (sp.Player_body, se.Enemy_body):
        snake.reset()
    frame = None
    field_array = None
    cur_char = None
    cur_stage = None
    isended = None
    gw.clear_world()
    gw.clear_collision_pairs()

def draw_all():
    global field_array, frame
    clear_canvas()
    gw.field_array = field_array_reset()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()
    # pprint(game_world.field_array)

def update():
    for objs in gw.all_objects_copy():
        objs.update()
    gw.rotate_object(se.Enemy_body.move_times, 'enemy')

    for a, b, group in gw.all_collision_pairs():
        if cm.collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)

    sp.Player_body.get_longer()
    sp.Player_body.get_shorter()
    is_game_ended()

frame = None
field_array = None
cur_char = None
cur_stage = None
isended = None