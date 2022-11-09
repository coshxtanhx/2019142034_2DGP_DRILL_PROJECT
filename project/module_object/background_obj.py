from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH

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

class Title_text():
    frame = 0
    image = None
    def __init__(self):
        pass
    def draw(self):
        self.image.draw()

class Title_message():
    frame = 0
    image = None
    def __init__(self):
        pass
    def __draw(self):
        pass