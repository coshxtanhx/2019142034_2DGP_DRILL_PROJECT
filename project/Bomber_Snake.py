from coordinates_module import UI_HEIGHT, UI_WIDTH
from pico2d import *
open_canvas(UI_WIDTH, UI_HEIGHT)

from state_changer import *
state_changer_activate('select_char')
#