from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from module_object.buttons_obj import *
from module_object.background_obj import *
from module_other.event_table_module import *
import module_other.state_changer
import module_other.game_world

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            module_other.state_changer.change_state('', None)
        elif event == KESCD:
            module_other.state_changer.change_state('snake_move', 'resume')
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if(button_clicked == 0):
                module_other.state_changer.change_state('title', 'exitall')
            elif(button_clicked == 1):
                from module_state.snake_move import cur_char, cur_stage
                module_other.state_changer.change_state('snake_move', 'exitall', \
                    cur_char + cur_stage)
            elif(button_clicked == 2):
                module_other.state_changer.change_state('option_setting', 'pause')
            elif(button_clicked == 3):
                module_other.state_changer.change_state('snake_move', 'resume')

def enters(option):
    global img_ui_bg, img_ui_text, buttons
    img_ui_bg = Background('menu')
    img_ui_text = Blinking_message('menu')
    buttons = [Game_menu_button(190 + 180 * i) for i in range(4)]
    module_other.game_world.add_object(img_ui_bg, 'bg')
    module_other.game_world.add_object(img_ui_text, 'obj')

def exits():
    global img_ui_bg, img_ui_text, buttons
    img_ui_bg = None
    img_ui_text = None
    buttons = None
    module_other.game_world.clear_world()

def draw_all():
    clear_canvas()
    for objs in module_other.game_world.all_objects():
        objs.draw()
    update_canvas()

def update():
    for objs in module_other.game_world.all_objects():
        objs.update()

img_ui_bg = None
img_ui_text = None
buttons = None