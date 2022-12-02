from module_other.coordinates_module import *
from module_other.term_table import *
from pico2d import *

class Circle_button:
    def isclicked(self, x, y):
        if(get_distance(x, y, *convert_coordinates(self.x, self.y)) < self.r):
            return True
        else:
            return False

class Game_menu_button(Circle_button):
    def __init__(self, x):
        self.x = x
        self.y = 330
        self.r = 60

class Option_volume_button(Circle_button):
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.clicked = False
        if(Option_volume_button.image == None):
            Option_volume_button.image = load_image('img/option_button.png')
    def isclicked(self, x, y):
        if(get_distance(x, y, self.x, UI_HEIGHT - self.y) < 12):
            self.clicked = True
            return True
        else:
            return False
    def draw(self):
        self.image.draw(self.x, self.y)
    def drag_move(self, x):
        self.x = clamp(256, x, 664)

class Close_book_button(Circle_button):
    def __init__(self):
        self.x = 802
        self.y = 544
        self.r = 30