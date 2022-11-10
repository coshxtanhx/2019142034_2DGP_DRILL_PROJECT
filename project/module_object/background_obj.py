from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH
from math import *

class Background():
    image_main = None
    image_menu = None
    image_play = None
    image_selc = None
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
        self.image = eval('Background.image_' + self.type)
    def draw(self):
        self.image.draw(UI_WIDTH//2, UI_HEIGHT//2)
    def update(self):
        pass

class Title_text():
    image = None
    def __init__(self, num):
        self.frame = 0
        if Title_text.image == None:
            Title_text.image = [load_image('img/title_' + str(i) + '.png') \
                for i in range(2)]
        self.image = Title_text.image[num]
        self.num = num
    def draw(self):
        self.image.draw(UI_WIDTH // 2, \
            520 - self.num * 120 + 5 * sin(radians(self.frame * 2)))
    def update(self):
        self.frame = (self.frame + 1) % 180

class Blinking_message():
    image_main = None
    image_menu = None
    def __init__(self, type):
        self.frame = 0
        self.type = type
        self.y = None
        if self.type == 'main':
            self.y = 220
        elif self.type == 'menu':
            self.y = 520
        if(Blinking_message.image_main == None and self.type == 'main'):
            Blinking_message.image_main = load_image('img/title_text.png')
        elif(Blinking_message.image_menu == None and self.type == 'menu'):
            Blinking_message.image_menu = load_image('img/field_menu_msg.png')
        self.image = eval('Blinking_message.image_' + self.type)
    def draw(self):
        if (self.frame % 90) < 45:
            self.image.draw(UI_WIDTH // 2, self.y)
    def update(self):
        self.frame = (self.frame + 1) % 180

class Option_ui():
    image = None
    def __init__(self):
        if Option_ui.image == None:
            Option_ui.image = load_image('img/option_ui.png')
    def draw(self):
        self.image.draw(UI_WIDTH//2, UI_HEIGHT//2)