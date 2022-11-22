from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH

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