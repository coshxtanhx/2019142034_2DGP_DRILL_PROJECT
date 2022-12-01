from module_other.coordinates_module import *
from module_other.term_table import *
import module_other.game_framework as gf
import module_other.server as sv

class Mine_field:
    def __init__(self, parent, dx, dy):
        self.parent = parent
        self.gx = parent.gx + dx
        self.gy = parent.gy + dy
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
    def update(self):
        pass
    def draw(self):
        pass
    def handle_collision(self, other, group):
        if group == COL_PHEAD_MINEFIELD:
            if self.parent.collided: return
            self.parent.collided = True

    def delete_from_server(self):
        sv.mine_field.remove(self)