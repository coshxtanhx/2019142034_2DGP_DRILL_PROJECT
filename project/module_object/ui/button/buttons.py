from module_other.coordinates_module import UI_WIDTH, UI_HEIGHT, get_distance
from pico2d import *

class Title_button:
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

class Game_menu_button:
    def __init__(self, x):
        self.x = x
        self.y = 330
        self.enabled = True
    def isclicked(self, x, y):
        if(get_distance(x, y, self.x, self.y) < 60):
            return True
        else:
            return False

class Option_volume_line:
    def __init__(self, y):
        self.x = UI_WIDTH // 2
        self.y = y
    def isclicked(self, x, y):
        if((self.x - 216 <= x <= self.x + 216) and \
            (UI_HEIGHT - (self.y + 7) < y < UI_HEIGHT - (self.y - 7))):
            return True
        else:
            return False

class Option_button:
    def __init__(self, x):
        self.x = x
        self.y = 230
    def isclicked(self, x, y):
        if((self.x - 70 <= x <= self.x + 70) and \
            (UI_HEIGHT - (self.y + 35) < y < UI_HEIGHT - (self.y - 35))):
            return True
        else:
            return False

class Option_volume_button:
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
            
class Start_and_Guide_Button:
    def __init__(self, x):
        self.x = x
        self.y = UI_HEIGHT - 525
    def isclicked(self, x, y):
        if((self.x - 145 <= x <= self.x + 145) and \
            (UI_HEIGHT - (self.y + 65) < y < UI_HEIGHT - (self.y - 65))):
            return True
        else:
            return False

class Char_sel_button:
    def __init__(self, x):
        self.x = x
        self.y = UI_HEIGHT - 277
    def isclicked(self, x, y):
        if((self.x - 27 <= x <= self.x + 27) and \
            (UI_HEIGHT - (self.y + 33) < y < UI_HEIGHT - (self.y - 33))):
            return True
        else:
            return False

class Next_page_button:
    def __init__(self, num):
        self.num = num
        if self.num == 1:
            self.x, self.y = 774, 107
        else:
            self.x, self.y = 133, 100
    def isclicked(self, x, y):
        if((self.x - 40 <= x <= self.x + 40) and \
            (UI_HEIGHT - (self.y + 16) < y < UI_HEIGHT - (self.y - 16))):
            return True
        else:
            return False

class Close_book_button:
    def __init__(self):
        self.x = 802
        self.y = 544
    def isclicked(self, x, y):
        if(get_distance(x, y, self.x, UI_HEIGHT - self.y) < 30):
            self.clicked = True
            return True
        else:
            return False

class Game_end_button:
    image = [None, None, None]
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        if(Game_end_button.image[self.n] == None):
            Game_end_button.image[self.n] = \
                load_image('img/clear_button_ui_' + str(self.n) + '.png')
    def draw(self):
        self.image[self.n].draw(self.x, self.y)
    def isclicked(self, x, y):
        if((self.x - 140 <= x <= self.x + 140) and \
            (UI_HEIGHT - (self.y + 65) < y < UI_HEIGHT - (self.y - 65))):
            return True
        else:
            return False
    def update(self):
        pass