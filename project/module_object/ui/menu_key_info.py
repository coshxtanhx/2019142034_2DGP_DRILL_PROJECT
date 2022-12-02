from math import ceil
from pico2d import *
import module_other.server as sv

class Menu_key_info:
    image = None
    def __init__(self):
        if Menu_key_info.image == None:
            Menu_key_info.image = load_image('img/menu_info.png')
    def draw(self):
        Menu_key_info.image.draw(810, 595)
    def update(self):
        pass
    def delete_from_server(self):
        sv.info = None