from module_other.coordinates_module import *
import module_other.server as sv

class Wall:
    def __init__(self, gx, gy):
        self.x, self.y = grid_to_coordinates(gx, gy)
    def update(self):
        pass
    def handle_collision(self, other, group):
        pass
    def draw(self):
        pass
    def delete_from_server(self):
        sv.wall = None