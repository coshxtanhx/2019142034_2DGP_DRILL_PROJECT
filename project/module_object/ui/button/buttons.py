from module_other.coordinates_module import *
from pico2d import *

class Circle_button:
    def isclicked(self, x, y):
        if(get_distance(x, y, *convert_coordinates(self.x, self.y)) < self.r):
            return True
        else:
            return False

class Rect_button:
    def isclicked(self, x, y):
        return is_in_rect(x, y, self.x, self.y, self.w, self.h)

class Title_button(Rect_button):
    def __init__(self, image, y):
        self.image = image
        self.x = UI_WIDTH//2
        self.y = y
        self.enabled = True
    def isclicked(self, x, y):
        if(self.enabled and (self.x - 197 < x < self.x + 197) and \
            (UI_HEIGHT - (self.y + 50) < y < UI_HEIGHT - (self.y - 50))):
            return True
        else:
            return False
    def draw(self):
        self.image.draw(UI_WIDTH // 2, self.y)

class Game_menu_button(Circle_button):
    def __init__(self, x):
        self.x = x
        self.y = 330
        self.r = 60

class Option_volume_line(Rect_button):
    def __init__(self, y):
        self.x = UI_WIDTH // 2
        self.y = y
        self.w = 216
        self.h = 7

class Option_button(Rect_button):
    def __init__(self, x):
        self.x = x
        self.y = 230
        self.w = 70
        self.h = 35

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
        if(self.clicked):
            self.x = clamp(256, x, 664)
            
class Start_and_Guide_Button(Rect_button):
    def __init__(self, x):
        self.x = x
        self.y = UI_HEIGHT - 525
        self.w = 145
        self.h = 65

class Char_sel_button(Rect_button):
    def __init__(self, x):
        self.x = x
        self.y = UI_HEIGHT - 277
        self.w = 27
        self.h = 33

class Next_page_button(Rect_button):
    def __init__(self, num):
        self.num = num
        if self.num == 1:
            self.x, self.y = 774, 107
        else:
            self.x, self.y = 133, 100
        self.w = 40
        self.h = 16

class Close_book_button(Circle_button):
    def __init__(self):
        self.x = 802
        self.y = 544
        self.r = 30

class Game_end_button(Rect_button):
    image = [None for _ in range(3)]
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        if(Game_end_button.image[self.n] == None):
            Game_end_button.image[self.n] = \
                load_image('img/clear_button_ui_' + str(self.n) + '.png')
        self.w = 140
        self.h = 65
    def draw(self):
        self.image[self.n].draw(self.x, self.y)
    def update(self):
        pass