from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH

class Clear_ui:
    image = None
    def __init__(self):
        if Clear_ui.image == None:
            Clear_ui.image = load_image('img/clear_ui.png')
    def draw(self):
        self.image.draw(UI_WIDTH//2, UI_HEIGHT//2 + 60)
    def update(self):
        pass