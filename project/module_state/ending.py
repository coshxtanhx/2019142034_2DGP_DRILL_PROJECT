from pico2d import *
from module_object.buttons_obj import *
from module_other.event_table_module import *
from module_object.background_obj import *
from module_object.star_obj import *
from module_object.rank_obj import *
import module_other.state_changer as sc
import module_other.game_world as gw

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            sc.change_state('', None)
        elif raw_event.type == SDL_KEYDOWN:
            sc.change_state('title', None)

def load_score(n):
    try:
        file = open('datas/savestar' + n + '.txt', 'r')
        num = int(file.read())
    except:
        return 0
    return num

def enters(option):
    star_sum = 0
    for i in '1234':
        star_sum += load_score(i)
    gw.add_object(Background('ends'), 0)
    gw.add_object(Rank(star_sum), 1)

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
star_sum = 0