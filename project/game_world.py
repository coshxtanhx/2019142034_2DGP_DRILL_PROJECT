# from pico2d import *

world = [[], [], []]

def all_objects():
    for layer in world:
        for o in layer:
            yield o

def add_object(o, depth):
    world[depth].append(o)

def remove_object(o):
    for layer in world:
        if(o in layer):
            layer.remove(o)
            del(o)
            return
    raise ValueError('value error')