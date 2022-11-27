from module_other.coordinates_module import *
from pico2d import *
import module_other.game_world as gw
import module_other.game_framework as gf
from module_other.term_table import *
import module_other.server as sv

class Skin_wall:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.remove_timer = 10
        if(Skin_wall.image == None):
            Skin_wall.image = load_image('img/snake_skinwall.png')
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
        if group in (COL_EHEAD_SKINWALL, COL_PHEAD_SKINWALL, COL_EXPLOSION_SKINWALL):
            gw.remove_object(self)
    def delete_from_server(self):
        sv.skin_wall.remove(self)