# from pico2d import *

DEPTH_DICT = {
    'bg': 0, 'obj': 1, 'player': 2, 'enemy': 3,
    'explode': 4, 'hider': 5 ,'ui': 6
}

world = dict()
cur_world = None

world['title'] = [[], [], [], [], [], []]
world['title_menu'] = [[], [], [], [], [], []]
world['snake_move'] = [[], [], [], [], [], []]
world['select_char'] = [[], [], [], [], [], []]
world['option_setting'] = [[], [], [], [], [], []]
world['how_to_play'] = [[], [], [], [], [], []]
world['game_menu'] = [[], [], [], [], [], []]

def all_objects():
    for layer in world[cur_world]:
        for o in layer:
            yield o

def add_object(o, depth):
    world[cur_world][DEPTH_DICT[depth]].append(o)

def add_objects(ol, depth):
    world[cur_world][DEPTH_DICT[depth]] += ol

def remove_object(o):
    for layer in world[cur_world]:
        if(o in layer):
            layer.remove(o)
            del(o)
            return
    raise ValueError('value error')