from module_other.coordinates_module import *
from pico2d import *
import module_other.game_world as gw

class Explosion:
    image = None
    def __init__(self, gx, gy, damage):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.frame = 6
        self.damage = damage
        if(Explosion.image == None):
            Explosion.image = load_image('img/explode.png')
    def draw(self):
        self.image.clip_draw(60 * (self.frame // 2), 0, 60, 60, self.x, self.y)
    def update(self):
        self.frame -= 1
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