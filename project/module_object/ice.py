from module_other.coordinates_module import *
from pico2d import *
import module_other.game_world as gw
import module_other.game_framework as gf

class Ice:
    image = None
    def __init__(self, gx, gy):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
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
    def check_col(self):
        cur_loc = gw.field_array[self.gx][self.gy]
        if cur_loc & (FIELD_DICT['player']):
            import module_object.snake_player
            module_object.snake_player.Player_body.get_damaged()
        if cur_loc & (FIELD_DICT['player'] + FIELD_DICT['enemy'] \
            + FIELD_DICT['explode']):
            gw.remove_object(self)