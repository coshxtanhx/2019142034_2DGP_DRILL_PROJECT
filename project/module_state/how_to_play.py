from pico2d import *
from module_object.buttons_obj import *
from module_other.event_table_module import *
from module_object.background_obj import Background, Book_page
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
            module_other.state_changer.change_state('select_char', 'resume')
        elif event == MLD:
            button_clicked = -1
            for i in range(3):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if button_clicked == 0:
                Book_page.change_page(-1)
            if button_clicked == 1:
                Book_page.change_page(+1)
            elif button_clicked == 2:
                module_other.state_changer.change_state('select_char', 'resume')

def enters(option):
    global bg, book, cur_selecting, buttons
    bg = Background('howt')
    cur_selecting = 0
    book = Book_page()
    buttons = [Next_page_button(i) for i in range(2)] + [Close_book_button()]
    module_other.game_world.add_object(bg, 'bg')
    module_other.game_world.add_object(book, 'obj')

def exits():
    global bg, book, cur_selecting, buttons
    bg = None
    book = None
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
book = None
cur_selecting = None
buttons = None