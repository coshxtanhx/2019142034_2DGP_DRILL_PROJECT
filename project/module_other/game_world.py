# from pico2d import *
from collections import deque
from module_other.coordinates_module import *

DEPTH_DICT = dict()
obj_list = [
    'bg', 'obj', 'bomb', 'player', 'enemy',
    'explode', 'ice', 'hider', 'ui'
]
obj_list_len = len(obj_list)

cnt = 0
for obj_name in obj_list:
    DEPTH_DICT[obj_name] = cnt
    cnt += 1

field_array = field_array_reset()

world = dict()
cur_world = None

state_list = [
    'title', 'title_menu', 'select_char',
    'option_setting', 'how_to_play', 'game_menu',
    'game_clear', 'game_over', 'ending'
] #snake_move is not included

for state_name in state_list:
    world[state_name] = [[] for _ in range(obj_list_len)]

world['play_state'] = []
for obj_name in obj_list:
    if obj_name == 'bg' or obj_name == 'ice' or obj_name == 'ui':
        world['play_state'] += [[]]
    else:
        world['play_state'] += [deque()]

def all_objects():
    for layer in world[cur_world]:
        for o in layer:
            yield o

def all_objects_copy():
    for layer in world[cur_world]:
        for o in layer.copy():
            yield o

def all_collision_objects():
    for layer_index in range(obj_list_len):
        if layer_index in (0,7,8):
            continue
        for o in world[cur_world][layer_index].copy():
            yield o

def add_object(o, depth):
    if type(depth) == int:
        depth = obj_list[depth]
    world[cur_world][DEPTH_DICT[depth]].append(o)

def add_objects(ol, depth):
    if type(depth) == int:
        depth = obj_list[depth]
    world[cur_world][DEPTH_DICT[depth]] += ol

def addleft_object(o, depth):
    if(type(world[cur_world][DEPTH_DICT[depth]]) != deque):
        print('Error: unable to use appendleft')
        return
    world[cur_world][DEPTH_DICT[depth]].appendleft(o)

def rotate_object(i, depth):
    if(type(world[cur_world][DEPTH_DICT[depth]]) != deque):
        print('Error: unable to use rotate')
        return
    world[cur_world][DEPTH_DICT[depth]].rotate(i)

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

def pop_object(depth):
    world[cur_world][DEPTH_DICT[depth]].pop()