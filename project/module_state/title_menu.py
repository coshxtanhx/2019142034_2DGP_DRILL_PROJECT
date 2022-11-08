from pico2d import *
from module_object.buttons_obj import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from event_table_module import *
import state_changer

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
    global acting, next_module, next_module_option
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
    global frame, img_title_bg, buttons
    global img_menu_button, file
    frame = 0
    img_title_bg = load_image('img/title_bg.png')
    img_menu_button[0] = load_image('img/title_menu_newgame.png')
    img_menu_button[1], loaded_suc = is_able_load()
    img_menu_button[2] = load_image('img/title_menu_option.png')
    img_menu_button[3] = load_image('img/title_menu_quit.png')
    buttons = [Title_button(img_menu_button[i], 550 - i * 150)\
        for i in range(4)]
    buttons[1].enabled = loaded_suc

def exits():
    global frame, buttons, img_menu_button, img_title_bg
    global file, loaded_dat
    frame = None
    img_title_bg = None
    buttons = None
    if(loaded_dat != 'failed'):
        file.close()
    file = None
    loaded_dat = None

def draw_all():
    clear_canvas()
    img_title_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    for button in buttons:
        button.draw()
    update_canvas()

def update():
    pass #Null Func

frame = None
img_title_bg = None
img_menu_button = [0,0,0,0]
buttons = None
file = None
loaded_dat = None