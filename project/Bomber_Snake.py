from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from pico2d import open_canvas, close_canvas
from module_other.state_changer import state_changer_activate

open_canvas(UI_WIDTH, UI_HEIGHT)
state_changer_activate('title')
close_canvas()
#