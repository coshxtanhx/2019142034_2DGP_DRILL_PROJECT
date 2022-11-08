from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from module_object.buttons_obj import *
from event_table_module import *
import state_changer

def handle_events():
    global img_ui_check_mark
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            state_changer.change_state('', None)
        elif event == KESCD:
            state_changer.change_state('snake_move', 'resume')
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if(button_clicked == 0):
                state_changer.change_state('title', 'exitall')
            elif(button_clicked == 1):
                from module_state.snake_move import cur_char, cur_stage
                file = open('savedata.txt', 'w')
                file.write(cur_char + cur_stage)
                file.close()
                img_ui_check_mark = load_image('img/check_saved.png')
            elif(button_clicked == 2):
                state_changer.change_state('option_setting', 'pause')
            elif(button_clicked == 3):
                state_changer.change_state('snake_move', 'resume')

def enters(option):
    global frame, img_ui_bg, img_ui_text, img_ui_check_mark, buttons
    frame = 0
    img_ui_bg = load_image('img/field_menu.png')
    img_ui_text = load_image('img/field_menu_msg.png')
    img_ui_check_mark = None
    buttons = [Game_menu_button(190 + 180 * i) for i in range(4)]

def exits():
    global frame, img_ui_bg, img_ui_text, buttons, img_ui_check_mark
    frame = None
    img_ui_bg = None
    img_ui_text = None
    img_ui_check_mark = None
    buttons = None

def draw_all():
    global frame
    clear_canvas()
    img_ui_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    if(frame < 45): img_ui_text.draw(UI_WIDTH // 2, 520)
    if(img_ui_check_mark): img_ui_check_mark.draw(370, 310)
    update_canvas()

def update():
    global frame
    frame = (frame + 1) % 90

frame = None
img_ui_bg = None
img_ui_text = None
img_ui_check_mark = None
buttons = None