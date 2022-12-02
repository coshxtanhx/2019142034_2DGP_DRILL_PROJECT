from pico2d import *
from module_object.ui.button.rect_button import *
from module_other.event_table_module import *
from module_object.ui.background import Background
from module_object.ui.clear import Clear_ui
from module_object.ui.star import *
from module_other.term_table import *
import module_other.game_framework as gf
import module_other.game_world as gw
import module_other.save_file_manager as sfm
import module_other.sound_manager as sm

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        ex, ey = raw_event.x, raw_event.y
        if event == QUIT:
            gf.change_state('', None)
        elif event == KESCD:
            gf.change_state('title', None)
        elif event == MLD:
            isclicked = None
            for i in range(2):
                if buttons[i].isclicked(ex, ey):
                    isclicked = i
                    break
            if isclicked == 0 and sfm.save_file.cur_stage != ENDING:
                gf.change_state('title', None)
            elif isclicked == 1:
                if sfm.save_file.cur_stage == ENDING:
                    gf.change_state('ending', None)
                else:
                    gf.change_state('play_state', None)

def enter():
    global buttons
    sm.bgm.stop()
    gw.add_object(Background('menu'), 0)
    gw.add_object(Clear_ui(), 1)
    buttons = [Game_end_button(272 + 377*i, 115, i) for i in range(2)]
    gw.add_objects(buttons, 1)
    star_num = sfm.end_state.get_star_num()
    gw.add_objects([Star(i) for i in range(star_num)], 2)
    sfm.save_cur_state()

def exit():
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    for objs in gw.all_objects():
        objs.update()

cur_game_data = None
buttons = None
stars = None