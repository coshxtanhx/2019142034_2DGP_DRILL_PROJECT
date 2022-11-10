from pico2d import *
from module_object.buttons_obj import *
from event_table_module import *
from module_object.background_obj import Background, Book_page
import state_changer
import game_world

def handle_events():
    global cur_selecting
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            state_changer.change_state('', None)
        elif event == KESCD:
            state_changer.change_state('select_char', 'resume')
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if button_clicked == 0:
                pass
            if button_clicked == 1:
                pass
            elif button_clicked == 2:
                pass
            elif button_clicked == 3:
                pass

def enters(option):
    global bg, book, cur_selecting, buttons
    bg = Background('howt')
    cur_selecting = 0
    book = Book_page()
    buttons = [Start_and_Guide_Button(x) for x in (250, 670)] \
        + [Char_sel_button(x) for x in (260, 660)]
    game_world.add_object(bg, 'bg')
    game_world.add_object(book, 'obj')

def exits():
    global bg, book, cur_selecting, buttons
    bg = None
    book = None
    cur_selecting = None
    buttons = None
    game_world.clear_world()

def draw_all():
    clear_canvas()
    for objs in game_world.all_objects():
        objs.draw()
    update_canvas()

def update():
    pass

bg = None
book = None
cur_selecting = None
buttons = None