from coordinates_module import *
from pico2d import *
import enemy_ai_list.apple_hunter

class apple():
    image = None
    def __init__(self, gx, gy):
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.exist = True
        if apple.image == None:
            apple.image = load_image('img/apple.png')
    def draw(self, field_array):
        if(self.exist):
            self.image.draw(self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['apple']
            global apple_gx, apple_gy
            enemy_ai_list.apple_hunter.apple_gx = self.gx
            enemy_ai_list.apple_hunter.apple_gy = self.gy
        else: return
        