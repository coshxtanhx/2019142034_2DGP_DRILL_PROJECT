from pico2d import *
from title_buttons_ui import *
from coordinates_module import UI_HEIGHT, UI_WIDTH

def is_able_load():
    global file
    try:
        file = open('savedata.txt', 'r')
    except:
        return load_image('img/title_menu_load_unable.png'), False
    else:
        return load_image('img/title_menu_loadgame.png'), True

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
                button_clicked = -1
                for i in range(4):
                    if(buttons[i].isclicked(event.x, event.y)):
                        button_clicked = i
                        break
                if(button_clicked == 0):
                    acting = False
                    next_module = 'snake_move'
                elif(button_clicked == 1):
                    acting = False
                    next_module = 'snake_move'
                elif(button_clicked == 2):
                    acting = False
                    next_module = 'snake_move'
                elif(button_clicked == 3):
                    acting = False
                    next_module = ''

def enters():
    global acting, frame, next_module, img_title_bg, buttons
    global img_menu_button, file
    acting = True
    frame = 0
    next_module = ''
    img_title_bg = load_image('img/title_bg.png')
    img_menu_button[0] = load_image('img/title_menu_newgame.png')
    img_menu_button[1], loaded = is_able_load()
    img_menu_button[2] = load_image('img/title_menu_option.png')
    img_menu_button[3] = load_image('img/title_menu_quit.png')
    buttons = [title_button(img_menu_button[i], 550 - i * 150)\
        for i in range(4)]
    buttons[1].enabled = loaded

def exits():
    global acting, frame, next_module, buttons, img_menu_button, img_title_bg
    global file
    acting = None
    frame = None
    next_module = None
    img_title_bg = None
    buttons = None
    file = None

def acts():
    global next_module
    enters()
    while(acting):
        clear_canvas()
        img_title_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        for button in buttons:
            button.draw()
        update_canvas()
        handle_events()
        delay(0.01)
    return next_module

acting = None
frame = None
next_module = None
img_title_bg = None
img_menu_button = [0,0,0,0]
buttons = None
file = None