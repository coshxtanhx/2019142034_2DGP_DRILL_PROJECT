# from pico2d import *

DEPTH_DICT = {
    'bg': 0, 'obj': 1, 'player': 2, 'enemy': 3,
    'explode': 4, 'hider': 5 ,'ui': 6
}

world = dict()
cur_world = None

state_list = [
    'title', 'title_menu', 'snake_move', 'select_char',
    'option_setting', 'how_to_play', 'game_menu'
]

for state_name in state_list:
    world[state_name] = [[] for _ in range(len(DEPTH_DICT))]

def all_objects():
    for layer in world[cur_world]:
        for o in layer:
            yield o

def add_object(o, depth):
    world[cur_world][DEPTH_DICT[depth]].append(o)

def add_objects(ol, depth):
    world[cur_world][DEPTH_DICT[depth]] += ol

def clear_world():
    for layer in world[cur_world]:
        layer.clear()

def remove_object(o):
    for layer in world[cur_world]:
        if(o in layer):
            layer.remove(o)
            del(o)
            return
    raise ValueError('value error')