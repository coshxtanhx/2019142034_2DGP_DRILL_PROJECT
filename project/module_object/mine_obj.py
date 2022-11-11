from coordinates_module import *
from pico2d import *

class Mine():
    image = None
    def __init__(self, field_array):
        self.counter = 40
        self.destructing = False
        self.sweeping = 180
        self.gx, self.gy = creatable_loc(field_array)
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        if Mine.image == None:
            Mine.image = load_image('img/mine.png')
    def draw(self, field_array):
        if self.counter <= 0:
            self.sweeped()
            return
        self.image.draw(self.x, self.y)
        field_array[self.gx+1][self.gy+1] |= FIELD_DICT['mine']
    def is_snake_here(self, field_array):
        if self.destructing:
            self.counter -= 1
            return
        for x in range(-1, 2, 1):
            for y in range(-1, 2, 1):
                if field_array[self.gx+1+x][self.gy+1+y] & FIELD_DICT['player']:
                    self.counter -= 1
                    self.destructing = True
                    break
    def sweeped(self):
        self.sweeping = int(self.sweeping * 0.9)
        self.image.clip_draw(0,0,180,180, self.x, self.y, self.sweeping, self.sweeping)
