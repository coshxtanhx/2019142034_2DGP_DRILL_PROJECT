from pico2d import *
from module_other.event_table_module import *
from module_object.ui.background import *
from module_object.rank import *
import module_other.game_framework as gf
import module_other.game_world as gw

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            gf.change_state('', None)
        elif raw_event.type == SDL_KEYDOWN:
            gf.change_state('title', None)

def remove_data():
    file = open('data/savedata.txt', 'w')
    file.write('')
    file.close()

def load_score(n):
    try:
        file = open('data/savestar' + n + '.txt', 'r')
        num = int(file.read())
    except:
        return 0
    return num

def enter():
    star_sum = 0
    for i in '1234':
        star_sum += load_score(i)
    gw.add_object(Background('ends'), 0)
    gw.add_object(Rank(star_sum), 1)
    remove_data()

def exit():
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
star_sum = 0