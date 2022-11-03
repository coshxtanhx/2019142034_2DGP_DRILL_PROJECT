from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from module_object.buttons_obj import *
from event_table_module import *

def handle_events():
    global acting, next_module, next_module_option, img_ui_check_mark
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            acting = False
            next_module, next_module_option = '', None
        elif event == KESCD:
            acting = False
            next_module, next_module_option = 'snake_move', 'resume'
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if(button_clicked == 0):
                acting = False
                next_module, next_module_option = 'title', 'exitall'
            elif(button_clicked == 1):
                from module_state.snake_move import cur_char, cur_stage
                file = open('savedata.txt', 'w')
                file.write(cur_char + cur_stage)
                file.close()
                img_ui_check_mark = load_image('img/check_saved.png')
            elif(button_clicked == 2):
                acting = False
                next_module, next_module_option = 'option_setting', 'pause'
            elif(button_clicked == 3):
                acting = False
                next_module, next_module_option = 'snake_move', 'resume'

def enters(option):
    global acting, next_module, next_module_option
    global frame, img_ui_bg, img_ui_text, img_ui_check_mark, buttons
    acting = True
    next_module = ''
    next_module_option = None
    frame = 0
    img_ui_bg = load_image('img/field_menu.png')
    img_ui_text = load_image('img/field_menu_msg.png')
    img_ui_check_mark = None
    buttons = [Game_menu_button(190 + 180 * i) for i in range(4)]

def exits():
    global acting, next_module, next_module_option
    global frame, img_ui_bg, img_ui_text, buttons, img_ui_check_mark
    acting = None
    next_module = None
    next_module_option = None
    frame = None
    img_ui_bg = None
    img_ui_text = None
    img_ui_check_mark = None
    buttons = None

def acts():
    global frame
    while(acting):
        clear_canvas()
        img_ui_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        if(frame < 45): img_ui_text.draw(UI_WIDTH // 2, 520)
        if(img_ui_check_mark): img_ui_check_mark.draw(370, 310)
        handle_events()
        update_canvas()
        frame = (frame + 1) % 90
        delay(0.01)
    return next_module, next_module_option

acting = None
next_module = ''
next_module_option = None
frame = None
img_ui_bg = None
img_ui_text = None
img_ui_check_mark = None
buttons = None