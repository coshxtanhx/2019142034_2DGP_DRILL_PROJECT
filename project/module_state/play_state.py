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
from module_object.wall import *
from module_object.ui.background import *
import module_other.game_framework as gf
import module_other.game_world as gw
import module_other.sound_manager as sm
import module_other.collision_manager as cm
import module_other.server as sv
import module_other.data_manager as dm
from pprint import pprint

def is_game_ended():
    if isended == DEFEAT:
        dm.end_state = dm.EndState(cur_char, cur_stage, None)
        gf.change_state('game_over', None)
    elif isended == VICTORY:
        dm.end_state = dm.EndState(cur_char, cur_stage, sv.player.length)
        gf.change_state('game_clear', 'exitall')
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
        if raw_event.key == SDLK_p: sv.enemy.get_damaged(125)

def enter():
    global cur_char, cur_stage, isended
    cur_char = dm.save_file.cur_character
    cur_stage = dm.save_file.cur_stage
    isended = STILL_PLAYING

    for x in range(15):
        sv.wall.append(Wall(x, -1))
        sv.wall.append(Wall(x, 9))
    for y in range(9):
        sv.wall.append(Wall(-1, y))
        sv.wall.append(Wall(15, y))

    sv.bg = Background('play')
    sv.player = sp.Player(cur_char)
    sv.player_head = sp.Player_head()
    sv.apple = create_first_apple()
    sv.enemy = se.Enemy(cur_stage)
    sv.enemy_head = se.Enemy_head()
    sv.hp_bar = HP_bar(cur_stage)

    gw.add_object(sv.bg, 'bg')
    gw.add_object(sv.player, 'player')
    gw.add_object(sv.player_head, 'player')
    gw.addleft_object(sv.apple, 'obj')
    gw.add_object(sv.enemy, 'enemy')
    gw.add_object(sv.enemy_head, 'enemy')
    gw.add_object(sv.hp_bar, 'ui')
    gw.add_objects(sv.wall, 0)
    sm.bgm = sm.Stage_bgm(cur_stage)

def exit():
    global isended, cur_char, cur_stage
    cur_char = None
    cur_stage = None
    isended = None
    gw.clear_world()
    gw.clear_collision_pairs()

def draw_all():
    clear_canvas()
    gw.field_array = field_array_reset()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()
    #pprint(gw.field_array)

def update():
    for objs in gw.all_objects_copy():
        objs.update()

    for a, b, group in gw.all_collision_pairs():
        if cm.collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)

    is_game_ended()

cur_char = None
cur_stage = None
isended = None