from random import randint
from pico2d import *
from math import ceil
import module_other.game_world as gw
import module_other.game_framework as gf

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
    blinking_period = 0.06
    def __init__(self):
        self.remove_timer = 3.6
        self.blinking_timer = 0
        if Screen_off.image1 == None:
            Screen_off.image1 = load_image('img/screen_off_0.png')
            Screen_off.image2 = load_image('img/screen_off_1.png')
    def draw(self):
        if self.remove_timer > 2.4 and ceil(self.blinking_timer * 15) % 2: return
        if self.remove_timer < 0.3 and ceil(self.blinking_timer * 15) % 2: return
        import module_object.snake_player as sp
        x, y = sp.Player_body.hx, sp.Player_body.hy
        self.image1.draw(x, y)
        self.image2.draw(x + 615, y)
        self.image2.draw(x - 615, y)
    def update(self):
        self.remove_timer -= gf.elapsed_time
        self.blinking_timer = (self.blinking_timer + gf.elapsed_time) % \
            (Screen_off.blinking_period * 2)
        if self.remove_timer <= 0:
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
        self.x -= gf.elapsed_time * 70
        if self.x < -165:
            gw.addleft_object(Cloud(), 'hider')
            gw.remove_object(self)
    def check_col(self):
        pass