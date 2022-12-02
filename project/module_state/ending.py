from pico2d import *
from module_other.event_table_module import *
from module_object.ui.background import *
from module_object.ui.rank import *
import module_other.game_framework as gf
import module_other.game_world as gw
import module_other.data_manager as dm

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            gf.change_state('', None)
        elif raw_event.type == SDL_KEYDOWN:
            gf.change_state('title', None)

def enter():
    star_sum = dm.save_file.number_of_stars
    gw.add_object(Background('ends'), 0)
    gw.add_object(Rank(star_sum), 1)
    dm.remove_save_data()

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

buttons = None