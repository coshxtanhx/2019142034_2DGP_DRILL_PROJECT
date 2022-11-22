from pico2d import *
from module_object.ui.button.buttons import *
from module_other.event_table_module import *
from module_object.ui.background import *
import module_other.state_changer as sc
import module_other.game_world as gw

def is_able_load():
    global file, loaded_dat
    try:
        file = open('data/savedata.txt', 'r')
        filestring = file.read(2)
        if filestring[0] not in ('1','2','3','4'): 1/0
        if filestring[1] not in ('1','2','3','4','5'): 1/0
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
            sc.change_state('', None)
        elif event == KESCD:
            sc.change_state('title', None)
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if(button_clicked == 0):
                sc.change_state('select_char', None)
            elif(button_clicked == 1):
                sc.change_state('play_state', None, loaded_dat)
            elif(button_clicked == 2):
                sc.change_state('option_setting', 'pause')
            elif(button_clicked == 3):
                sc.change_state('', None)

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
    gw.add_object(title_bg, 1)
    gw.add_objects(buttons, 2)

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
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
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