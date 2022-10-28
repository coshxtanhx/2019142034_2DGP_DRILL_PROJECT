from pico2d import *

class HP_bar():
    image_bar = None
    image_text = None
    def __init__(self, num):
        if HP_bar.image_bar == None:
            HP_bar.image_bar = load_image('img/hp_bar0.png')
            HP_bar.image_text = \
                [load_image('img/enemy_name_' + str(i) + '.png') for i in range(4)]
        self.num = num
    def draw(self, enemy_hp):
        self.image_bar.clip_draw(0, 0, 40, 40, \
            100 + (enemy_hp//4), 590, enemy_hp//2, 40)
        self.image_text[self.num].draw(50, 590)