from pico2d import *
from module_object.ui.button.rect_button import *
from module_object.ui.button.circle_button import *
from module_object.ui.background import Background
from module_object.ui.blinking_msg import Blinking_message
from module_other.event_table_module import *
import module_other.game_framework as gf
import module_other.game_world as gw

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            gf.change_state('', None)
        elif event == KESCD:
            gf.change_state('play_state', 'resume')
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if(button_clicked == 0):
                gf.change_state('title', 'exitall')
            elif(button_clicked == 1):
                from module_state.play_state import cur_char, cur_stage
                gf.change_state('play_state', 'exitall')
            elif(button_clicked == 2):
                gf.change_state('option_setting', 'pause')
            elif(button_clicked == 3):
                gf.change_state('play_state', 'resume')

def enter():
    global img_ui_bg, img_ui_text, buttons
    img_ui_bg = Background('menu')
    img_ui_text = Blinking_message('menu')
    buttons = [Game_menu_button(190 + 180 * i) for i in range(4)]
    gw.add_object(img_ui_bg, 'bg')
    gw.add_object(img_ui_text, 'obj')

def exit():
    global img_ui_bg, img_ui_text, buttons
    img_ui_bg = None
    img_ui_text = None
    buttons = None
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    for objs in gw.all_objects():
        objs.update()

img_ui_bg = None
img_ui_text = None
buttons = None