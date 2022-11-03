from random import randint
from pico2d import *

class Broken():
    image = None
    def __init__(self):
        self.x = randint(70, 70+780)
        self.y = randint(70, 70+420)
        self.shape = randint(0, 3)
        if Broken.image == None:
            Broken.image = load_image('img/broken_screen.png')
    def draw(self):
        self.image.clip_draw(self.shape * 240, 0, 240, 240, \
            self.x, self.y)

class Screen_off():
    image1 = None
    image2 = None
    def __init__(self):
        if Screen_off.image1 == None:
            Screen_off.image1 = load_image('img/screen_off_0.png')
            Screen_off.image2 = load_image('img/screen_off_1.png')
    def draw(self, x, y):
        self.image1.draw(x, y)
        self.image2.draw(x + 615, y)
        self.image2.draw(x - 615, y)

class Cloud():
    image = None
    def __init__(self):
        self.x = 920 - 700
        self.y = randint(70, 420+70)
        if Cloud.image == None:
            Cloud.image = load_image('img/cloud.png')
    def draw(self):
        self.image.draw(self.x, self.y)
        self.x -= 1