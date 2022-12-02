from module_other.coordinates_module import *
from module_other.term_table import *
from pico2d import *

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

class Game_end_button(Rect_button):
    image = [None for _ in range(4)]
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        import module_other.data_manager as dm
        if dm.save_file.cur_stage == STAGE4 and self.n == 0: self.n = 3
        if(Game_end_button.image[self.n] == None):
            Game_end_button.image[self.n] = \
                load_image('img/clear_button_ui_' + str(self.n) + '.png')
        self.w = 140
        self.h = 65
    def draw(self):
        self.image[self.n].draw(self.x, self.y)
    def update(self):
        pass