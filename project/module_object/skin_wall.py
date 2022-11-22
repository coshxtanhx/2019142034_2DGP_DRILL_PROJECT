from module_other.coordinates_module import *
from pico2d import *
import module_other.game_world as gw

class Skin_wall:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.frame = 700
        if(Skin_wall.image == None):
            Skin_wall.image = load_image('img/snake_skinwall.png')
    def draw(self):
        gw.field_array[self.gx][self.gy] |= FIELD_DICT['ice']
        drawframe = (701 - self.frame) if (self.frame > 694) else 6
        drawframe = (self.frame + 1) if (self.frame < 5) else drawframe
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, \
            10 * drawframe, 10 * drawframe)
    def update(self):
        self.frame -= 1
        if self.frame <= 0:
            gw.remove_object(self)
    def check_col(self):
        cur_loc = gw.field_array[self.gx+1][self.gy+1]
        if cur_loc & (FIELD_DICT['head']):
            import module_object.snake_player
            module_object.snake_player.Blue_body.get_damaged()
        if cur_loc & (FIELD_DICT['head'] + FIELD_DICT['enemy'] \
            + FIELD_DICT['explode']):
            gw.remove_object(self)