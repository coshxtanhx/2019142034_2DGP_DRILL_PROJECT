from module_other.coordinates_module import *
from pico2d import *
import module_other.server as sv
import module_other.game_framework as gf
import module_other.game_world as gw
from random import *

PIXEL_PER_MM = (1.0 / 1.6)  # 1 pixel 1.6 mm
MOVE_SPEED_MMPS = 600
MOVE_SPEED_PPS = (MOVE_SPEED_MMPS * PIXEL_PER_MM)

NUMBER_OF_FRAGMENTS = 20

def create_fragments(obj, bigger=False):
    sv.fragment += [Fragment(obj.gx, obj.gy) for _ in range(NUMBER_OF_FRAGMENTS)]
    gw.add_objects(sv.fragment[-1:-1-NUMBER_OF_FRAGMENTS:-1], 'fragment')
    for i in range(8):
        x, y = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1)][i]
        sv.fragment += [Fragment(obj.gx+x, obj.gy+y) \
            for _ in range(NUMBER_OF_FRAGMENTS)]
        gw.add_objects(sv.fragment[-1:-1-NUMBER_OF_FRAGMENTS:-1], 'fragment')


class Fragment:
    image = None
    def __init__(self, gx, gy):
        if Fragment.image == None:
            Fragment.image = load_image('img/fragment.png')
        self.x, self.y = grid_to_coordinates(gx, gy)
        self.dx, self.dy = 0, 0
        self.vx = choice((-1,1)) * randint(10, 30)
        self.vy = 30
        self.a = 30 / ((self.vx) ** 2)
        self.direction = 1 if (self.vx > 0) else -1
    def update(self):
        self.dx += self.direction * gf.elapsed_time * MOVE_SPEED_PPS
        self.dy = self.get_y_from_parabola_func()
        if self.y + self.dy <= -5:
            gw.remove_object(self)
    def draw(self):
        Fragment.image.draw(self.x + self.dx, self.y + self.dy)
    def delete_from_server(self):
        sv.fragment.remove(self)
    def get_y_from_parabola_func(self):
        return -self.a*(self.dx - self.vx)**2 + self.vy