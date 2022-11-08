from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from event_table_module import *
from math import *
import state_changer

def handle_events():
    global next_module, acting
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
    global img_title, img_title_bg, img_title_text
    frame = 0
    img_title_bg = load_image('img/title_bg.png')
    img_title = [load_image('img/title_' + str(i) + '.png') for i in range(2)]
    img_title_text = load_image('img/title_text.png')

def exits():
    global img_title, img_title_bg, img_title_text
    img_title_bg = None
    img_title = None
    img_title_text = None

def draw_all():
    clear_canvas()
    img_title_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    img_title[0].draw(UI_WIDTH // 2, 520 + 5 * sin(radians(frame * 2)))
    img_title[1].draw(UI_WIDTH // 2, 400 + 5 * sin(radians(frame * 2)))
    if (frame % 90) < 45: img_title_text.draw(UI_WIDTH // 2, UI_HEIGHT // 2 - 100)
    update_canvas()

def update():
    global frame
    frame = (frame + 1) % 180

img_title_bg = None
img_title = None
img_title_text = None