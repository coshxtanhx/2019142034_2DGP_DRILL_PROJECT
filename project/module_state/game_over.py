from pico2d import *
from module_object.ui.button.rect_button import *
from module_other.event_table_module import *
from module_object.ui.background import Background
from module_object.ui.blinking_msg import Blinking_message
import module_other.game_framework as gf
from module_other.term_table import *
import module_other.game_world as gw
import module_other.sound_manager as sm

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        ex, ey = raw_event.x, raw_event.y
        if event == QUIT:
            gf.change_state('', None)
        elif event == KESCD:
            gf.change_state('title', 'exitall')
        elif event == MLD:
            isclicked = None
            for i in range(2):
                if buttons[i].isclicked(ex, ey):
                    isclicked = i
                    break
            if isclicked == 0:
                gf.change_state('title', 'exitall')
            elif isclicked == 1:
                gf.change_state('play_state', None)

def enter():
    global buttons
    sm.bgm.stop()
    gw.add_object(Background('over'), 0)
    gw.add_object(Blinking_message('over'), 1)
    buttons = [Game_end_button(270 + 190*i, 150, i) for i in (0,2)]
    gw.add_objects(buttons, 1)

def exit():
    global buttons
    buttons = None
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    for objs in gw.all_objects():
        objs.update()

buttons = None
cur_game_data = None