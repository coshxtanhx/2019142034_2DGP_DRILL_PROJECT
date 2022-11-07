from pico2d import *
from module_object.buttons_obj import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from event_table_module import *
from module_object.background_obj import Background

def handle_events():
    global acting, next_module, next_module_option
    global cur_selecting
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            acting = False
            next_module, next_module_option = '', None
        elif event == KESCD:
            acting = False
            next_module, next_module_option = 'title_menu', None
        elif event == MLD:
            button_clicked = -1
            for i in range(4):
                if(buttons[i].isclicked(raw_event.x, raw_event.y)):
                    button_clicked = i
                    break
            if button_clicked == 0:
                acting = False
                next_module, next_module_option = \
                    'snake_move', str(cur_selecting+1) + '1'
            if button_clicked == 1:
                acting = False
                next_module, next_module_option = \
                    'how_to_play', 'pause'
            elif button_clicked == 2:
                cur_selecting = (cur_selecting + 3) % 4
            elif button_clicked == 3:
                cur_selecting = (cur_selecting + 1) % 4
            print(cur_selecting)

def enters(option):
    global bg, selection_images, cur_selecting, buttons
    bg = Background('selc')
    selection_images = [load_image('img/select_char_' + str(i) + '.png') \
        for i in range(4)]
    cur_selecting = 0
    buttons = [Start_and_Guide_Button(x) for x in (250, 670)] \
        + [Char_sel_button(x) for x in (260, 660)]

def exits():
    global acting, next_module, next_module_option
    global bg, selection_images, cur_selecting, buttons
    acting = None
    next_module = None
    next_module_option = None
    bg = None
    selection_images = None
    cur_selecting = None
    buttons = None

def acts():
    while(acting):
        clear_canvas()
        bg.draw()
        selection_images[cur_selecting].draw(UI_WIDTH//2, UI_HEIGHT - 275)
        update_canvas()
        handle_events()
        delay(0.01)
    return next_module, next_module_option

acting = None
next_module = None
next_module_option = None
bg = None
selection_images = None
cur_selecting = None
buttons = None