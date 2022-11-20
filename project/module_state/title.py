from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from module_other.event_table_module import *
from module_object.background_obj import *
from math import *
import module_other.game_world as gw
import module_other.state_changer as sc

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            sc.change_state('', None)
        elif event == KSD:
            sc.change_state('title_menu', None)
        elif event == KESCD:
            sc.change_state('', None)

def enters(option):
    global img_title_msg, img_title_bg, img_title_text
    img_title_bg = Background('main')
    img_title_text = [Title_text(num) for num in range(2)]
    img_title_msg = Blinking_message('main')
    gw.add_object(img_title_bg, 0)
    gw.add_objects(img_title_text, 1)
    gw.add_object(img_title_msg, 1)


def exits():
    global img_title_msg, img_title_bg, img_title_text
    img_title_bg = None
    img_title_msg = None
    img_title_text = None
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    for objs in gw.all_objects():
        objs.update()

img_title_bg = None
img_title_msg = None
img_title_text = None