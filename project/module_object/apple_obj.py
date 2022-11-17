from module_other.coordinates_module import *
from pico2d import *
import module_enemy_ai.apple_hunter
import module_other.game_world

poisoned = False
mode = None

def create_first_apple():
    global mode, poisoned
    from module_state.snake_move import cur_char
    mode = cur_char
    poisoned = True if (mode == '2') else False
    return Normal_apple(10, 0)

def create_new_apple():
    global poisoned
    if poisoned:
        poisoned = False
        return Poison_apple()
    else:
        poisoned = bool(mode == '2')
        return Normal_apple()

class Apple():
    def check_col(self):
        cur_loc = module_other.game_world.field_array[self.gx+1][self.gy+1]
        if cur_loc & (FIELD_DICT['head'] + FIELD_DICT['ehead'] \
            + FIELD_DICT['explode']):
            module_other.game_world.remove_object(self)
            module_other.game_world.addleft_object(create_new_apple(), 'obj')
    def update(self):
        pass

class Normal_apple(Apple):
    image = None
    def __init__(self, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = creatable_loc(module_other.game_world.field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = False
        self.exist = True
        if Normal_apple.image == None:
            Normal_apple.image = load_image('img/apple.png')
    def draw(self):
        if(self.exist):
            self.image.draw(self.x, self.y)
            module_other.game_world.field_array[self.gx+1][self.gy+1] \
                |= FIELD_DICT['apple']
            module_enemy_ai.apple_hunter.apple_gx = self.gx
            module_enemy_ai.apple_hunter.apple_gy = self.gy
        else: return

class Poison_apple(Apple):
    image = None
    def __init__(self, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = creatable_loc(module_other.game_world.field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = True
        self.exist = True
        if Poison_apple.image == None:
            Poison_apple.image = load_image('img/apple_poison.png')
    def draw(self):
        if(self.exist):
            self.image.draw(self.x, self.y)
            module_other.game_world.field_array[self.gx+1][self.gy+1] \
                |= FIELD_DICT['poison']
            module_enemy_ai.apple_hunter.apple_gx = -65535
        else: return
        