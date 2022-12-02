from module_other.coordinates_module import *
from pico2d import *
from module_other.term_table import *
import module_other.game_world as gw
import module_other.game_framework as gf
import module_other.server as sv

class Explosion:
    image = None
    def __init__(self, gx, gy, damage):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        self.remove_timer = 0.1
        self.damage = damage
        if(Explosion.image == None):
            Explosion.image = load_image('img/explode.png')
    def draw(self):
        drawing_size = (int(600 * (0.1 - self.remove_timer)),) * 2
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, *drawing_size)
        gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['explode']
    def update(self):
        self.remove_timer -= gf.elapsed_time
        if self.remove_timer <= 0:
            gw.remove_object(self)
    def handle_collision(self, other, group):
        pass
    def delete_from_server(self):
        sv.explosion.remove(self)