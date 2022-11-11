from coordinates_module import *
from pico2d import *
from random import choice
import module_enemy_ai.apple_hunter
import game_world

poisoned = False

def create_first_apple(mode):
    global poisoned
    poisoned = True if (mode == '2') else False
    return Normal_apple(10, 0)

def create_new_apple(mode):
    global poisoned
    if poisoned:
        poisoned = False
        return Poison_apple()
    else:
        poisoned = bool(mode == '2')
        return Normal_apple()

class Normal_apple():
    image = None
    def __init__(self, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = creatable_loc(game_world.field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = False
        self.exist = True
        if Normal_apple.image == None:
            Normal_apple.image = load_image('img/apple.png')
    def draw(self):
        if(self.exist):
            self.image.draw(self.x, self.y)
            game_world.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['apple']
            module_enemy_ai.apple_hunter.apple_gx = self.gx
            module_enemy_ai.apple_hunter.apple_gy = self.gy
        else: return

class Poison_apple():
    image = None
    def __init__(self, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = creatable_loc(game_world.field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = True
        self.exist = True
        if Poison_apple.image == None:
            Poison_apple.image = load_image('img/apple_poison.png')
    def draw(self):
        if(self.exist):
            self.image.draw(self.x, self.y)
            game_world.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['poison']
            module_enemy_ai.apple_hunter.apple_gx = -65535
        else: return
        