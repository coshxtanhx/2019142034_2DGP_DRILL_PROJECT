# from pico2d import *

DEPTH_DICT = {
    'bg': 0, 'obj': 1, 'player': 2, 'enemy': 3,
    'explode': 4, 'hider': 5 ,'ui': 6
}

world = [[], [], [], [], [], []]

def all_objects():
    for layer in world:
        for o in layer:
            yield o

def add_object(o, depth):
    world[DEPTH_DICT[depth]].append(o)

def add_objects(ol, depth):
    world[DEPTH_DICT[depth]] += ol

def remove_object(o):
    for layer in world:
        if(o in layer):
            layer.remove(o)
            del(o)
            return
    raise ValueError('value error')