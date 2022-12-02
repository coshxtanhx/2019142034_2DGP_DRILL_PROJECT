from pico2d import *
from module_object.ui.button.buttons import *
from module_other.event_table_module import *
from module_object.ui.background import *
import module_other.game_framework as gf
import module_other.game_world as gw
import module_other.data_manager as dm

def is_able_load():
    is_valid_file = dm.load_cur_state()
    if is_valid_file:
        return load_image('img/title_menu_loadgame.png'), True
    else:
        return load_image('img/title_menu_load_unable.png'), False

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            gf.change_state('', None)
        elif event == KESCD:
            gf.change_state('title', None)
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if(button_clicked == 0):
                gf.change_state('select_char', None)
            elif(button_clicked == 1):
                gf.change_state('play_state', None)
            elif(button_clicked == 2):
                gf.change_state('option_setting', 'pause')
            elif(button_clicked == 3):
                gf.change_state('', None)

def enter():
    global title_bg, buttons
    global img_menu_button
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

def exit():
    global buttons, img_menu_button, title_bg
    title_bg = None
    buttons = None
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    pass

title_bg = None
img_menu_button = [0,0,0,0]
buttons = None