from pico2d import *
from module_object.ui.button.rect_button import *
from module_other.event_table_module import *
from module_other.term_table import *
from module_object.ui.background import Background
from module_object.ui.selection import Selection
import module_other.game_framework as gf
import module_other.game_world as gw
import module_other.data_manager as dm

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            gf.change_state('', None)
        elif event == KESCD:
            gf.change_state('title_menu', None)
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if button_clicked == 0:
                dm.save_file = dm.SaveFile(Selection.num)
                gf.change_state('play_state', None)
            if button_clicked == 1:
                gf.change_state('how_to_play', 'pause')
            elif button_clicked == 2:
                Selection.change_img(-1)
            elif button_clicked == 3:
                Selection.change_img(+1)

def enter():
    global bg, selection_images, buttons
    bg = Background('selc')
    selection_images = Selection()
    buttons = [Start_and_Guide_Button(x) for x in (250, 670)] \
        + [Char_sel_button(x) for x in (260, 660)]
    gw.add_object(bg, 0)
    gw.add_object(selection_images, 1)

def exit():
    global bg, selection_images, buttons
    bg = None
    selection_images = None
    buttons = None
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    pass

bg = None
selection_images = None
buttons = None