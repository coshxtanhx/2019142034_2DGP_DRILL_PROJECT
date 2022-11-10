from pico2d import *
from module_object.buttons_obj import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from event_table_module import *
from module_object.background_obj import *
import state_changer
import game_world

def is_able_load():
    global file, loaded_dat
    try:
        file = open('savedata.txt', 'r')
        filestring = file.read(2)
        for i in range(2):
            if filestring[i] not in ('1','2','3','4'): 1/0
    except:
        loaded_dat = 'failed'
        return load_image('img/title_menu_load_unable.png'), False
    else:
        loaded_dat = filestring[0:2]
        return load_image('img/title_menu_loadgame.png'), True

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            state_changer.change_state('', None)
        elif event == KESCD:
            state_changer.change_state('title', None)
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if(button_clicked == 0):
                state_changer.change_state('select_char', None)
            elif(button_clicked == 1):
                state_changer.change_state('snake_move', loaded_dat)
            elif(button_clicked == 2):
                state_changer.change_state('option_setting', 'pause')
            elif(button_clicked == 3):
                state_changer.change_state('', None)

def enters(option):
    global frame, title_bg, buttons
    global img_menu_button, file
    frame = 0
    title_bg = Background('main')
    img_menu_button[0] = load_image('img/title_menu_newgame.png')
    img_menu_button[1], loaded_suc = is_able_load()
    img_menu_button[2] = load_image('img/title_menu_option.png')
    img_menu_button[3] = load_image('img/title_menu_quit.png')
    buttons = [Title_button(img_menu_button[i], 550 - i * 150)\
        for i in range(4)]
    buttons[1].enabled = loaded_suc
    game_world.add_object(title_bg, 'bg')
    game_world.add_objects(buttons, 'ui')

def exits():
    global frame, buttons, img_menu_button, title_bg
    global file, loaded_dat
    frame = None
    title_bg = None
    buttons = None
    if(loaded_dat != 'failed'):
        file.close()
    file = None
    loaded_dat = None
    game_world.clear_world()

def draw_all():
    clear_canvas()
    for objs in game_world.all_objects():
        objs.draw()
    update_canvas()

def update():
    pass

frame = None
title_bg = None
img_menu_button = [0,0,0,0]
buttons = None
file = None
loaded_dat = None