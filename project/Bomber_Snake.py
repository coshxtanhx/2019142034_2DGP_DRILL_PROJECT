from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from pico2d import open_canvas
open_canvas(UI_WIDTH, UI_HEIGHT)

from module_other.state_changer import state_changer_activate
state_changer_activate('snake_move')
#