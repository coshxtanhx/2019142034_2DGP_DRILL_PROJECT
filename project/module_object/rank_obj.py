from pico2d import *

def star_num_to_rank(num):
    if num <= 4: return '4'
    if num <= 6: return '3'
    if num <= 8: return '2'
    if num <= 10: return '1'
    else: return '0'

class Rank():
    def __init__(self, num):
        self.num = num
        self.frame = 0
        self.image = load_image('img/rank_' + star_num_to_rank(num) + '.png')
    def draw(self):
        self.image.draw(540, 640 - 420)
    def update(self):
        pass