from module_other.coordinates_module import *
from pico2d import *
import module_other.game_world as gw
import module_other.time_manager as tm

class Ice:
    image = None
    def __init__(self, gx, gy):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.frame = 10
        if(Ice.image == None):
            Ice.image = load_image('img/ice.png')
    def draw(self):
        gw.field_array[self.gx][self.gy] |= FIELD_DICT['ice']
        drawframe = (701 - self.frame) if (self.frame > 694) else 6
        drawframe = (self.frame + 1) if (self.frame < 5) else drawframe
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, \
            10 * drawframe, 10 * drawframe)
    def update(self):
        self.frame -= tm.elapsed_time
        if self.frame <= 0:
            gw.remove_object(self)
    def check_col(self):
        cur_loc = gw.field_array[self.gx][self.gy]
        if cur_loc & (FIELD_DICT['player']):
            import module_object.snake_player
            module_object.snake_player.Player_body.get_damaged()
        if cur_loc & (FIELD_DICT['player'] + FIELD_DICT['enemy'] \
            + FIELD_DICT['explode']):
            gw.remove_object(self)