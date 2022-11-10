from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from module_object.buttons_obj import *
from module_object.background_obj import *
from event_table_module import *
import state_changer
import game_world

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
    img_ui_bg = Background('menu')
    img_ui_text = Blinking_message('menu')
    img_ui_check_mark = None
    buttons = [Game_menu_button(190 + 180 * i) for i in range(4)]
    game_world.add_object(img_ui_bg, 'bg')
    game_world.add_object(img_ui_text, 'obj')

def exits():
    global frame, img_ui_bg, img_ui_text, buttons, img_ui_check_mark
    frame = None
    img_ui_bg = None
    img_ui_text = None
    img_ui_check_mark = None
    buttons = None
    game_world.clear_world()

def draw_all():
    global frame
    clear_canvas()
    for objs in game_world.all_objects():
        objs.draw()
    if(img_ui_check_mark): img_ui_check_mark.draw(370, 310)
    update_canvas()

def update():
    for objs in game_world.all_objects():
        objs.update()

frame = None
img_ui_bg = None
img_ui_text = None
img_ui_check_mark = None
buttons = None