from module_other.coordinates_module import *
from pico2d import *
from module_object.bomb import *
from module_object.mine_field import *
from random import *
import module_other.game_world as gw
import module_other.server as sv
import module_other.game_framework as gf
import module_other.sound_manager as sm

class Mine:
    image = None
    def __init__(self):
        self.remove_counter = 0.57
        self.collided = False
        self.ready_to_explode = False
        self.never_explode = False
        self.drawing_size_rate = 0.5
        self.activated = False
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
                gw.add_object(sv.mine_field[-1], 'obj')
        sm.sound_effect.play(choice(SE_PIANO))

    def draw(self):
        self.image.clip_draw(0,0,180,180, self.x, self.y, \
            360*self.drawing_size_rate, 360*self.drawing_size_rate)

    def handle_collision(self, other, group):
        if group == COL_PHEAD_MINE:
            if self.never_explode: return
            self.explode()

    def explode(self):
        sv.bomb.appendleft(Bomb(self.x, self.y, 0, MINE_BOMB))
        gw.addleft_object(sv.bomb[0], 'bomb')
        gw.remove_object(self)

    def update(self):

        if self.remove_counter <= 0:
            self.ready_to_explode = True

        if (self.collided and not(self.ready_to_explode)) or\
            self.activated:
            self.activated = True
            self.remove_counter -= gf.elapsed_time

        if self.drawing_size_rate <= 0:
            gw.remove_object(self)

        if self.ready_to_explode and self.collided and not(self.never_explode):
            self.explode()
        
        elif not(self.never_explode) and \
            self.ready_to_explode and not(self.collided):
            sm.sound_effect.play(choice(SE_PIANO))
            self.never_explode = True

        if self.never_explode:
            self.drawing_size_rate -= gf.elapsed_time

        if self.collided:
            self.collided = False


    def delete_from_server(self):
        for i in range(8):
            gw.remove_object(self.child[i])
        sv.mine.remove(self)