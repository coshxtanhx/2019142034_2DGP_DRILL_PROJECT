from module_other.coordinates_module import *
from pico2d import *
import module_enemy_ai.apple_hunter
import module_other.game_world as gw
import module_other.server as sv
from module_object.fragment import *
from module_other.term_table import *

poisoned = 0
mode = None

def create_first_apple():
    global mode, poisoned
    from module_state.play_state import cur_char
    mode = cur_char
    poisoned = 1 if (mode == POISON_APPLE_SNAKE) else 0
    return Normal_apple(10, 0)

def create_new_apple():
    global poisoned
    if poisoned == 2:
        poisoned = 0
        return Poison_apple()
    else:
        poisoned = (poisoned + bool(mode == POISON_APPLE_SNAKE)) % 3
        return Normal_apple()

class Apple:
    def handle_collision(self, other, group):
        if group in (COL_PHEAD_APPLE, COL_EHEAD_APPLE, COL_APPLE_SKINWALL):
            self.get_removed()
        elif group in (COL_EXPLOSION_APPLE, COL_APPLE_ICE):
            create_fragments(self)
            self.get_removed()
    def update(self):
        pass
    def get_removed(self):
        gw.remove_object(self)
    def delete_from_server(self):
        sv.apple = create_new_apple()
        gw.addleft_object(sv.apple, 'obj')

class Normal_apple(Apple):
    image = None
    def __init__(self, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = creatable_loc(gw.field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = False
        self.exist = True
        if Normal_apple.image == None:
            Normal_apple.image = load_image('img/apple.png')
    def draw(self):
        if(self.exist):
            self.image.draw(self.x, self.y)
            gw.field_array[self.gx+1][self.gy+1] \
                |= FIELD_DICT['apple']
            module_enemy_ai.apple_hunter.apple_gx = self.gx
            module_enemy_ai.apple_hunter.apple_gy = self.gy
        else: return

class Poison_apple(Apple):
    image = None
    def __init__(self, gx = -1, gy = -1):
        if gx == -1:
            gx, gy = creatable_loc(gw.field_array)
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.gx, self.gy = gx, gy
        self.poisoned = True
        self.exist = True
        if Poison_apple.image == None:
            Poison_apple.image = load_image('img/apple_poison.png')
    def draw(self):
        if(self.exist):
            self.image.draw(self.x, self.y)
            gw.field_array[self.gx+1][self.gy+1] \
                |= FIELD_DICT['poison']
            module_enemy_ai.apple_hunter.apple_gx = -65535
        else: return
        