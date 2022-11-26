from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from pico2d import *
from module_other.game_framework import game_framework_activate

open_canvas(UI_WIDTH, UI_HEIGHT)
game_framework_activate('title')
close_canvas()