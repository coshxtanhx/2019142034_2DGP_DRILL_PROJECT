from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from math import *

class Title:
    image = None
    def __init__(self, num):
        self.frame = 0
        if Title.image == None:
            Title.image = [load_image('img/title_' + str(i) + '.png') \
                for i in range(2)]
        self.image = Title.image[num]
        self.num = num
    def draw(self):
        self.image.draw(UI_WIDTH // 2, \
            520 - self.num * 120 + 5 * sin(radians(self.frame * 2)))
    def update(self):
        self.frame = (self.frame + 1) % 180