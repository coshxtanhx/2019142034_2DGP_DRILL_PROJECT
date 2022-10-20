from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from math import *

img_title_bg = load_image('img/title_bg.png')
img_title = [load_image('img/title_' + str(i) + '.png') for i in range(2)]
img_title_text = load_image('img/title_text.png')

def handle_events():
    global next_module
    global acting
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            acting = False
            next_module = ''
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_s:
                acting = False
                next_module = 'title_menu'
            elif event.key == SDLK_ESCAPE:
                acting = False

def act():
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
    return next_module

next_module = ''
acting = True
frame = 0