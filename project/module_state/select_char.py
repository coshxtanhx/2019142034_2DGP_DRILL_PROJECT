from pico2d import *
from module_object.buttons_obj import *
from module_other.event_table_module import *
from module_object.background_obj import Background, Selection
import module_other.state_changer
import module_other.game_world

def handle_events():
    global cur_selecting
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            module_other.state_changer.change_state('', None)
        elif event == KESCD:
            module_other.state_changer.change_state('title_menu', None)
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if button_clicked == 0:
                module_other.state_changer.change_state('snake_move', None, \
                    str(Selection.num+1) + '1')
            if button_clicked == 1:
                module_other.state_changer.change_state('how_to_play', 'pause')
            elif button_clicked == 2:
                Selection.change_img(-1)
            elif button_clicked == 3:
                Selection.change_img(+1)

def enters(option):
    global bg, selection_images, cur_selecting, buttons
    bg = Background('selc')
    selection_images = Selection()
    cur_selecting = 0
    buttons = [Start_and_Guide_Button(x) for x in (250, 670)] \
        + [Char_sel_button(x) for x in (260, 660)]
    module_other.game_world.add_object(bg, 'bg')
    module_other.game_world.add_object(selection_images, 'obj')

def exits():
    global bg, selection_images, cur_selecting, buttons
    bg = None
    selection_images = None
    cur_selecting = None
    buttons = None
    module_other.game_world.clear_world()

def draw_all():
    clear_canvas()
    for objs in module_other.game_world.all_objects():
        objs.draw()
    update_canvas()

def update():
    pass

bg = None
selection_images = None
cur_selecting = None
buttons = None