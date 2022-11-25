from module_other.coordinates_module import *
from pico2d import *
import module_other.game_world as gw
import module_other.time_manager as tm

class Explosion:
    image = None
    def __init__(self, gx, gy, damage):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.frame = 0.1
        self.damage = damage
        if(Explosion.image == None):
            Explosion.image = load_image('img/explode.png')
    def draw(self):
        drawing_size = (int(600 * (0.1 - self.frame)),) * 2
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, *drawing_size)
    def update(self):
        self.frame -= tm.elapsed_time
        if self.frame <= 0:
            gw.remove_object(self)
    def check_col(self):
        if self.frame != 3:
            return
        cur_loc = gw.field_array[self.gx][self.gy]
        if cur_loc & (FIELD_DICT['enemy']):
            import module_object.snake_enemy as se
            se.Enemy_body.get_damaged(self.damage)
        if cur_loc & (FIELD_DICT['player']):
            import module_object.snake_player as sp
            sp.Player_body.get_damaged()