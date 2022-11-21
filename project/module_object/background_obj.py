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

class Title_text:
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

class Blinking_message:
    image_main = None
    image_menu = None
    image_over = None
    def __init__(self, type):
        self.frame = 0
        self.type = type
        self.y = None
        if self.type == 'main':
            self.y = 220
        elif self.type == 'menu':
            self.y = 520
        elif self.type == 'over':
            self.y = 450
        if(Blinking_message.image_main == None and self.type == 'main'):
            Blinking_message.image_main = load_image('img/title_text.png')
        elif(Blinking_message.image_menu == None and self.type == 'menu'):
            Blinking_message.image_menu = load_image('img/field_menu_msg.png')
        elif(Blinking_message.image_over == None and self.type == 'over'):
            Blinking_message.image_over = load_image('img/gameover_msg.png')
        self.image = eval('Blinking_message.image_' + self.type)
    def draw(self):
        if (self.frame % 90) < 45:
            self.image.draw(UI_WIDTH // 2, self.y)
    def update(self):
        self.frame = (self.frame + 1) % 180

class Option_ui:
    image = None
    def __init__(self):
        if Option_ui.image == None:
            Option_ui.image = load_image('img/option_ui.png')
    def draw(self):
        self.image.draw(UI_WIDTH//2, UI_HEIGHT//2)

class Selection:
    image = None
    num = 0
    def __init__(self):
        Selection.num = 0
        if Selection.image == None:
            Selection.image = [load_image('img/select_char_' + str(i) + '.png') \
        for i in range(4)]
    def draw(self):
        self.image[Selection.num].draw(UI_WIDTH//2, UI_HEIGHT - 275)
    def change_img(option):
        Selection.num = (Selection.num + option) % 4

class Book_page:
    MAX_PAGE = 6
    image = [None for _ in range(MAX_PAGE)]
    page = 0
    def __init__(self):
        Book_page.page = 0
        Book_page.load_new_image()
    def change_page(option):
        Book_page.page = (Book_page.page + option * 2) % Book_page.MAX_PAGE
        Book_page.load_new_image()
    def load_new_image():
        if Book_page.image[Book_page.page] == None:
            for i in range(2):
                Book_page.image[Book_page.page + i] = load_image('img/help' \
                    + str(Book_page.page//2) + str(i) + '.png')
    def draw(self):
        gap = 195
        for i in range(2):
            self.image[Book_page.page+i].draw(\
                UI_WIDTH//2 + gap*2*i - gap, UI_HEIGHT//2)

class Clear_ui:
    image = None
    def __init__(self):
        if Clear_ui.image == None:
            Clear_ui.image = load_image('img/clear_ui.png')
    def draw(self):
        self.image.draw(UI_WIDTH//2, UI_HEIGHT//2 + 60)
    def update(self):
        pass