from module_other.coordinates_module import *
from pico2d import *
from module_object.bomb import *
from module_object.mine_field import *
import module_other.game_world as gw
import module_other.server as sv
import module_other.game_framework as gf

class Mine:
    image = None
    def __init__(self):
        self.counter = 0.57
        self.destructing = False
        self.sweeping = 1
        self.gx, self.gy = creatable_loc(gw.field_array, 1)
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        if Mine.image == None:
            Mine.image = load_image('img/mine.png')
        self.child = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0: continue
                sv.mine_field.append(Mine_field(self, dx, dy))
                self.child.append(sv.mine_field[-1])
                gw.add_object(sv.mine_field[-1])

    def draw(self):
        self.image.clip_draw(0,0,180,180, self.x, self.y, \
            180*self.sweeping, 180*self.sweeping)
        gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['mine']
    def check_col(self):
        if self.counter <= 0: return
        if self.destructing and self.counter <= 0.02:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    cur_loc = gw.field_array[self.gx+1+x][self.gy+1+y]
                    if cur_loc & (FIELD_DICT['head']):
                        gw.add_object(Bomb(self.x, self.y, 0, 4), 'bomb')
                        gw.remove_object(self)
        else:
            cur_loc = gw.field_array[self.gx+1][self.gy+1]
            self.check_if_snake_here()
            if cur_loc & (FIELD_DICT['head']):
                gw.add_object(Bomb(self.x, self.y, 0, 4), 'bomb')
                gw.remove_object(self)
    def update(self):
        if self.destructing:
            self.counter -= gf.elapsed_time
        if self.counter <= 0: self.sweeping -= gf.elapsed_time
        if self.sweeping <= 0: gw.remove_object(self)
    def check_if_snake_here(self):
        if self.destructing:
            return
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0: continue
                if gw.field_array[self.gx+1+x][self.gy+1+y] \
                    & FIELD_DICT['head']:
                    self.destructing = True
                    break

    def delete_from_server(self):
        sv.mine.remove(self)