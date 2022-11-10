from math import *

def field_array_reset():
    field_array = [[16] * 11]
    for _ in range(0, 15):
        field_array += [[16] + [0] * 9 + [16]]
    field_array += [[16] * 11]
    return field_array

def button_pos_to_volume(x):
    return int((x - 256) / 408 * 128)

def volume_to_button_pos(vol):
    return int(vol / 128 * 408 + 256)

def get_distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def convert_coordinates(x, y):
    return x, UI_HEIGHT - y

def grid_to_coordinates(x, y):
    return (x * 60 + 40), UI_HEIGHT - (y * 60 + 120)

def coordinates_to_grid(x, y):
    return (x - 40 + 30) // 60, (-y + UI_HEIGHT - 120 + 30) // 60

UI_WIDTH, UI_HEIGHT = 920, 640
MAX_BITS = 16777215

FIELD_DICT = {
    'empty': 0, 'player': 1, 'enemy':2, 'apple':4, \
    'bomb':8, 'wall':16, 'head':32, 'explode': 64, 'skin': 128,\
    'box': 256, 'ice': 512, 'armor': 1024, 'poison': 2048
}

dx = (+5, +0, -5, +0)
dy = (+0, +5, +0, -5)