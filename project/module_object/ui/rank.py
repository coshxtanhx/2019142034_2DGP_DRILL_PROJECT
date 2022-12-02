from pico2d import *
from module_other.term_table import *

def star_num_to_rank(num):
    if num <= 4: return RANK_E
    if num <= 6: return RANK_D
    if num <= 8: return RANK_C
    if num <= 10: return RANK_B
    else: return RANK_A

class Rank:
    def __init__(self, star_num):
        self.star_num = star_num
        self.frame = 0
        self.image = load_image('img/rank_' + star_num_to_rank(star_num) + '.png')
    def draw(self):
        self.image.draw(540, 640 - 420)
    def update(self):
        pass