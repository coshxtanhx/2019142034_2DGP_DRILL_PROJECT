# from pico2d import *
from collections import deque
from module_other.coordinates_module import *
import module_other.collision_manager as cm

DEPTH_DICT = dict()
obj_list = [
    'bg', 'obj', 'bomb', 'player', 'enemy',
    'explode', 'breakable', 'hider', 'ui'
]
obj_list_len = len(obj_list)

cnt = 0
for obj_name in obj_list:
    DEPTH_DICT[obj_name] = cnt
    cnt += 1

field_array = field_array_reset()

world = dict()
collision_group = dict()
cur_world = None

state_list = [
    'title', 'title_menu', 'select_char',
    'option_setting', 'how_to_play', 'game_menu',
    'game_clear', 'game_over', 'ending'
] #play state is not included

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

def add_object(o, depth):
    if type(depth) == int:
        depth = obj_list[depth]
    world[cur_world][DEPTH_DICT[depth]].append(o)
    cm.add_collision_pairs_automatically(o)

def add_objects(ol, depth):
    if type(depth) == int:
        depth = obj_list[depth]
    world[cur_world][DEPTH_DICT[depth]] += ol
    cm.add_collision_pairs_automatically(ol, is_list=True)

def addleft_object(o, depth):
    if(type(world[cur_world][DEPTH_DICT[depth]]) != deque):
        print('Error: unable to use appendleft')
        return
    world[cur_world][DEPTH_DICT[depth]].appendleft(o)
    cm.add_collision_pairs_automatically(o)

def rotate_object(i, depth):
    if(type(world[cur_world][DEPTH_DICT[depth]]) != deque):
        print('Error: unable to use rotate')
        return
    world[cur_world][DEPTH_DICT[depth]].rotate(i)

def clear_world():
    for layer in world[cur_world]:
        layer.clear()

def clear_collision_pairs():
    global collision_group
    collision_group = dict()

def remove_object(o, auto_remove=True):
    for layer in world[cur_world]:
        if(o in layer):
            layer.remove(o)
            remove_collision_object(o)
            del(o)
            return

def pop_object(depth):
    o = world[cur_world][DEPTH_DICT[depth]].pop()
    remove_collision_object(o)


def add_collision_pairs(a, b, group):
    if group not in collision_group:
        collision_group[group] = [ [], [] ] # list of list : list pair

    if a:
        if type(a) is list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)

    if b:
        if type(b) is list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)

def all_collision_pairs():
    for group, pairs in (collision_group.copy()).items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group

def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)