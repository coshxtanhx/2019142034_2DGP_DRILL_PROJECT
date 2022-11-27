from math import ceil
from pico2d import *
import module_other.server as sv

class HP_bar:
    image_bar = None
    image_frame1 = None
    image_frame2 = None
    image_text = None
    def __init__(self, stage):
        if HP_bar.image_bar == None:
            HP_bar.image_bar = load_image('img/hp_bar0.png')
            HP_bar.image_text = \
                [load_image('img/enemy_name_' + str(i) + '.png') for i in range(4)]
            HP_bar.image_frame1 = load_image('img/hp_bar1.png')
            HP_bar.image_frame2 = load_image('img/hp_bar2.png')
        self.num = int(stage) - 1
    def draw(self):
        hp = sv.enemy.hp
        self.image_frame1.draw(105+160, 590)
        self.image_bar.clip_draw(0, 0, 40, 40, \
            105 + ceil(hp/6), 590, hp//3, 40)
        self.image_text[self.num].draw(55, 590)
        self.image_frame2.draw(105+160, 590)
    def update(self):
        pass
    def delete_from_server(self):
        sv.hp_bar = None