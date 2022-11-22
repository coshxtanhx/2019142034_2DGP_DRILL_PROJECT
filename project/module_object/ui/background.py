from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH
from math import *

class Background:
    image_main = None
    image_menu = None
    image_play = None
    image_selc = None
    image_howt = None
    image_over = None
    image_ends = None
    def __init__(self, type):
        self.type = type
        if(Background.image_main == None and self.type == 'main'):
            Background.image_main = load_image('img/title_bg.png')
        elif(Background.image_menu == None and self.type == 'menu'):
            Background.image_menu = load_image('img/field_menu.png')
        elif(Background.image_play == None and self.type == 'play'):
            Background.image_play = load_image('img/field.png')
        elif(Background.image_selc == None and self.type == 'selc'):
            Background.image_selc = load_image('img/character_select_bg.png')
        elif(Background.image_howt == None and self.type == 'howt'):
            Background.image_howt = load_image('img/book.png')
        elif(Background.image_over == None and self.type == 'over'):
            Background.image_over = load_image('img/black_screen.png')
        elif(Background.image_ends == None and self.type == 'ends'):
            Background.image_ends = load_image('img/ending_bg.png')
        self.image = eval('Background.image_' + self.type)
    def draw(self):
        self.image.draw(UI_WIDTH//2, UI_HEIGHT//2)
    def update(self):
        pass
    def check_col(self):
        pass