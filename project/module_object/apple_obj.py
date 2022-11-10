from coordinates_module import *
from pico2d import *
from random import choice
import module_enemy_ai.apple_hunter

poisoned = False

def create_first_apple(field_array, mode):
    global poisoned
    poisoned = True if (mode == '2') else False
    return Normal_apple(field_array, 10, 0)

def create_new_apple(field_array, mode):
    global poisoned
    if poisoned:
        poisoned = False
        return Poison_apple(field_array)
    else:
        poisoned = bool(mode == '2')
        return Normal_apple(field_array)

def new_apple_loc(field_array):
    able_to_create = []
    for x in range(0, 15):
        for y in range(0, 9):
            if(field_array[x+1][y+1] == 0):
                able_to_create.append((x,y))
    return choice(able_to_create)

class Normal_apple():
    image = None
    def __init__(self, field_array, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = new_apple_loc(field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = False
        self.exist = True
        if Normal_apple.image == None:
            Normal_apple.image = load_image('img/apple.png')
    def draw(self, field_array):
        if(self.exist):
            self.image.draw(self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['apple']
            module_enemy_ai.apple_hunter.apple_gx = self.gx
            module_enemy_ai.apple_hunter.apple_gy = self.gy
        else: return

class Poison_apple():
    image = None
    def __init__(self, field_array, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = new_apple_loc(field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = True
        self.exist = True
        if Poison_apple.image == None:
            Poison_apple.image = load_image('img/apple_poison.png')
    def draw(self, field_array):
        if(self.exist):
            self.image.draw(self.x, self.y)
            field_array[self.gx+1][self.gy+1] |= FIELD_DICT['poison']
            module_enemy_ai.apple_hunter.apple_gx = -65535
        else: return
        