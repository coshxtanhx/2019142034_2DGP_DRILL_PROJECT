from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from math import *
import module_other.game_framework as gf

class Title:
    image = None
    def __init__(self, num):
        self.timer = 0
        if Title.image == None:
            Title.image = [load_image('img/title_' + str(i) + '.png') \
                for i in range(2)]
        self.image = Title.image[num]
        self.num = num
    def draw(self):
        self.image.draw(UI_WIDTH // 2, \
            520 - self.num * 120 + 5 * sin(self.timer * 2.5))
    def update(self):
        self.timer += gf.elapsed_time