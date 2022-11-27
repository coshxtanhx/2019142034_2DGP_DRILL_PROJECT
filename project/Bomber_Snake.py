from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from pico2d import *
from module_other.game_framework import activate_game_framework

open_canvas(UI_WIDTH, UI_HEIGHT)
activate_game_framework('title')
close_canvas()