from module_other.coordinates_module import *

class Mine_field:
    def __init__(self, parent, dx, dy):
        self.parent = parent
        self.gx = parent.gx + dx
        self.gy = parent.gy + dy
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)