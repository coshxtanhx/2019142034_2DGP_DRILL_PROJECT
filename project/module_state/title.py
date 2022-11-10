from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from event_table_module import *
from module_object.background_obj import *
from math import *
import game_world
import state_changer

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            state_changer.change_state('', None)
        elif event == KSD:
            state_changer.change_state('title_menu', None)
        elif event == KESCD:
            state_changer.change_state('', None)

def enters(option):
    global frame
    global img_title_msg, img_title_bg, img_title_text
    frame = 0
    img_title_bg = Background('main')
    img_title_text = [Title_text(num) for num in range(2)]
    img_title_msg = Title_message()
    game_world.add_object(img_title_bg, 'bg')
    game_world.add_objects(img_title_text, 'obj')
    game_world.add_object(img_title_msg, 'obj')


def exits():
    global img_title_msg, img_title_bg, img_title_text
    img_title_bg = None
    img_title_msg = None
    img_title_text = None
    game_world.clear_world()

def draw_all():
    clear_canvas()
    for objs in game_world.all_objects():
        objs.draw()
    update_canvas()

def update():
    for objs in game_world.all_objects():
        objs.update()

img_title_bg = None
img_title_msg = None
img_title_text = None