from coordinates_module import *
from pico2d import *
from module_object.bomb_obj import *
from collections import deque

def check_is_snake_here(field_array, gx, gy, findhead=False):
    check_obj = FIELD_DICT['head'] if findhead else FIELD_DICT['player']
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            if field_array[gx+1+x][gy+1+y] & check_obj:
                return True
    return False

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
        if self.counter <= 0 and self.sweeping < 180 and \
            check_is_snake_here(field_array, self.gx, self.gy, True):
            for x in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    import module_state.snake_move
                    module_state.snake_move.explodes.appendleft(\
                        explosion(self.gx+1+x, self.gy+1+y, 0))
            module_state.snake_move.mine = Mine(field_array)
        elif self.counter <= 0:
            self.sweeped()
            return
        self.image.draw(self.x, self.y)
        field_array[self.gx+1][self.gy+1] |= FIELD_DICT['mine']
    def snake_is_here(self, field_array):
        if self.destructing:
            self.counter -= 1
            return
        if check_is_snake_here(field_array, self.gx, self.gy):
            self.counter -= 1
            self.destructing = True
    def sweeped(self):
        self.sweeping = int(self.sweeping * 0.9)
        self.image.clip_draw(0,0,180,180, self.x, self.y, self.sweeping, self.sweeping)
        if self.sweeping < 0.01:
            import module_state.snake_move
            module_state.snake_move.mine = Mine(module_state.snake_move.field_array)