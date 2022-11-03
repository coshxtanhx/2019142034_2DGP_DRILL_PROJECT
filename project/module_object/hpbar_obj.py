from math import ceil
from pico2d import *

class HP_bar():
    image_bar = None
    image_frame1 = None
    image_frame2 = None
    image_text = None
    def __init__(self, num):
        if HP_bar.image_bar == None:
            HP_bar.image_bar = load_image('img/hp_bar0.png')
            HP_bar.image_text = \
                [load_image('img/enemy_name_' + str(i) + '.png') for i in range(4)]
            HP_bar.image_frame1 = load_image('img/hp_bar1.png')
            HP_bar.image_frame2 = load_image('img/hp_bar2.png')
        self.num = num
    def draw(self, enemy_hp):
        self.image_frame1.draw(105+160, 590)
        self.image_bar.clip_draw(0, 0, 40, 40, \
            105 + ceil(enemy_hp/4), 590, enemy_hp//2, 40)
        self.image_text[self.num].draw(55, 590)
        self.image_frame2.draw(105+160, 590)