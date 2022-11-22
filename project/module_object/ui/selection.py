from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH

class Selection:
    image = None
    num = 0
    def __init__(self):
        Selection.num = 0
        if Selection.image == None:
            Selection.image = [load_image('img/select_char_' + str(i) + '.png') \
        for i in range(4)]
    def draw(self):
        self.image[Selection.num].draw(UI_WIDTH//2, UI_HEIGHT - 275)
    def change_img(option):
        Selection.num = (Selection.num + option) % 4