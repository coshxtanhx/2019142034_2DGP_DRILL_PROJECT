from pico2d import *
from module_object.buttons_obj import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from module_other.event_table_module import *
from module_object.background_obj import *
from module_object.star_obj import *
import module_other.state_changer as sc
import module_other.game_world as gw

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        ex, ey = raw_event.x, raw_event.y
        if event == QUIT:
            sc.change_state('', None)
        elif event == KESCD:
            sc.change_state('title', None)
        elif event == MLD:
            isclicked = None
            for i in range(2):
                if buttons[i].isclicked(ex, ey):
                    isclicked = i
                    break
            if isclicked == 0:
                sc.change_state('title', 'exitall')
            elif isclicked == 1:
                sc.change_state('snake_move', 'exitall', cur_game_data)

def get_stars(n):
    if n > 5: return 1
    if n > 1: return 2
    return 1

def saves(data):
    file = open('datas/savedata.txt', 'w')
    file.write(data)
    file.close()

    idx = str(int(data[1]) - 1)
    file = open('datas/savestar' + idx + '.txt', 'w')
    file.write(str(star_num))
    file.close()

def enters(option):
    if not(option):
        option = '114'
    global cur_game_data, buttons, star_num
    cur_game_data = option[:2]
    star_num = get_stars(int(option[2]))
    gw.add_object(Background('menu'), 0)
    gw.add_object(Clear_ui(), 1)
    buttons = [Game_end_button(272 + 377*i, 115, i) for i in range(2)]
    gw.add_objects(buttons, 1)
    gw.add_objects([Star(i) for i in range(star_num)], 2)
    saves(cur_game_data)

def exits():
    gw.clear_world()

def draw_all():
    clear_canvas()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    for objs in gw.all_objects():
        objs.update()

cur_game_data = None
buttons = None
stars = None
star_num = 0