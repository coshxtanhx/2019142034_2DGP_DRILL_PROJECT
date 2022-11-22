from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH

class Option_ui:
    image = None
    def __init__(self):
        if Option_ui.image == None:
            Option_ui.image = load_image('img/option_ui.png')
    def draw(self):
        self.image.draw(UI_WIDTH//2, UI_HEIGHT//2)