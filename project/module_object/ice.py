from module_other.coordinates_module import *
from pico2d import *
import module_other.game_world as gw
import module_other.game_framework as gf
from module_other.term_table import *
import module_other.server as sv
from module_object.fragment import *

class Ice:
    image = None
    def __init__(self, gx, gy):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        self.remove_timer = 10
        if(Ice.image == None):
            Ice.image = load_image('img/ice.png')
    def draw(self):
        gw.field_array[self.gx][self.gy] |= FIELD_DICT['ice']
        drawing_size = 0
        if self.remove_timer > 9.9: drawing_size = 10 - self.remove_timer
        elif self.remove_timer < 0.1: drawing_size = self.remove_timer
        else: drawing_size = 0.1
        drawing_size = (int(drawing_size * 600),) * 2
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, *drawing_size)
    def update(self):
        self.remove_timer -= gf.elapsed_time
        if self.remove_timer <= 0:
            gw.remove_object(self)
    def handle_collision(self, other, group):
        if group in (COL_ENEMY_ICE, COL_PLAYER_ICE, COL_EXPLOSION_ICE):
            create_fragments(self)
            gw.remove_object(self)
    def delete_from_server(self):
        sv.ice.remove(self)