from random import randint
from pico2d import *
import module_other.game_world as gw

class Broken:
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
    def update(self):
        pass
    def check_col(self):
        pass

class Screen_off:
    image1 = None
    image2 = None
    def __init__(self):
        self.frame = 220
        if Screen_off.image1 == None:
            Screen_off.image1 = load_image('img/screen_off_0.png')
            Screen_off.image2 = load_image('img/screen_off_1.png')
    def draw(self):
        if self.frame > 160 and ((self.frame-160) // 6) % 2 == 0:
            return
        import module_object.snake_player as sp
        x, y = sp.Player_body.hx, sp.Player_body.hy
        self.image1.draw(x, y)
        self.image2.draw(x + 615, y)
        self.image2.draw(x - 615, y)
    def update(self):
        self.frame -= 1
        if self.frame <= 0:
            gw.remove_object(self)
    def check_col(self):
        pass

class Cloud:
    image = None
    def __init__(self):
        self.x = 920 + 165
        self.y = randint(70, 420+70)
        if Cloud.image == None:
            Cloud.image = load_image('img/cloud.png')
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        self.x -= 1
        if self.x < -165:
            gw.addleft_object(Cloud(), 'hider')
            gw.remove_object(self)
    def check_col(self):
        pass