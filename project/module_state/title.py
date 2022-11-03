from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from event_table_module import *
from math import *

def handle_events():
    global next_module, acting
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            acting = False
            next_module = ''
        elif event == KSD:
            acting = False
            next_module = 'title_menu'
        elif event == KESCD:
            acting = False

def enters(option):
    global next_module, acting, frame
    global img_title, img_title_bg, img_title_text
    next_module = ''
    acting = True
    frame = 0
    img_title_bg = load_image('img/title_bg.png')
    img_title = [load_image('img/title_' + str(i) + '.png') for i in range(2)]
    img_title_text = load_image('img/title_text.png')

def exits():
    global next_module, acting, frame
    global img_title, img_title_bg, img_title_text
    next_module = None
    acting = None
    frame = None
    img_title_bg = None
    img_title = None
    img_title_text = None

def acts():
    global acting, frame
    acting = True
    while(acting):
        clear_canvas()
        img_title_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        img_title[0].draw(UI_WIDTH // 2, 520 + 5 * sin(radians(frame * 2)))
        img_title[1].draw(UI_WIDTH // 2, 400 + 5 * sin(radians(frame * 2)))
        if (frame % 90) < 45: img_title_text.draw(UI_WIDTH // 2, UI_HEIGHT // 2 - 100)
        frame = (frame + 1) % 180
        update_canvas()
        handle_events()
        delay(0.01)
    return next_module, None

next_module = None
acting = None
frame = None
img_title_bg = None
img_title = None
img_title_text = None