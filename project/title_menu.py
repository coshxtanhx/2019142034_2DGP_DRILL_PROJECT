from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH

def handle_events():
    global acting, next_module
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            acting = False
            next_module = ''
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                acting = False
                next_module = 'title'
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if (UI_WIDTH//2 - 197 < event.x < UI_WIDTH//2 + 197 and \
                    UI_HEIGHT - (520 + 50) < event.y < UI_HEIGHT - (520 - 50)):
                    acting = False
                    next_module = 'snake_move'

def enters():
    global acting, frame, next_module
    global img_menu_load, img_menu_new, img_title_bg, img_menu_quit
    acting = True
    frame = 0
    next_module = ''
    img_title_bg = load_image('img/title_bg.png')
    img_menu_new = load_image('img/title_menu_newgame.png')
    img_menu_load = load_image('img/title_menu_loadgame.png')
    img_menu_quit = load_image('img/title_menu_quit.png')

def exits():
    global acting, frame, next_module
    global img_menu_load, img_menu_new, img_title_bg, img_menu_quit
    acting = None
    frame = None
    next_module = None
    img_title_bg = None
    img_menu_new = None
    img_menu_load = None
    img_menu_quit = None

def acts():
    global next_module
    enters()
    while(acting):
        clear_canvas()
        img_title_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        img_menu_new.draw(UI_WIDTH // 2, 520)
        img_menu_load.draw(UI_WIDTH // 2, 370)
        img_menu_quit.draw(UI_WIDTH // 2, 220)
        update_canvas()
        handle_events()
        delay(0.01)
    return next_module

acting = None
frame = None
next_module = None
img_title_bg = None
img_menu_new = None
img_menu_load = None
img_menu_quit = None