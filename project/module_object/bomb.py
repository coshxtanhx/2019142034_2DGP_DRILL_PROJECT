from pico2d import *
from module_other.coordinates_module import *
from module_other.term_table import *
from module_object.ice import Ice
from module_object.explosion import Explosion
import module_other.game_world as gw
import module_other.sound_manager as sm
import module_other.game_framework as gf
import module_other.server as sv

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

ICE_REMOVER = FIELD_DICT['enemy'] + FIELD_DICT['explode'] \
    + FIELD_DICT['bomb'] + FIELD_DICT['apple'] + FIELD_DICT['ice']

class Bomb:
    image = None
    image2 = None
    image3 = None
    image4 = None
    def __init__(self, x, y, damage, option = 0):
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        self.counter = 5 if (option != MINE_BOMB) else 0
        self.damage = damage
        self.option = option
        self.frame = 0
        self.owner = ENEMY_OWNS if (self.damage == 0) else PLAYER_OWNS
        if Bomb.image == None:
            Bomb.image = \
                [load_image('img/bomb_' + str(i) + '.png') for i in range(1, 11)]
            Bomb.image2 = load_image('img/bomb_cross.png')
            Bomb.image3 = load_image('img/bomb_ice.png')
            Bomb.image4 = load_image('img/bomb_ice_cross.png')
    def update(self):
        self.counter -= gf.elapsed_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * gf.elapsed_time) % 3
        if(self.counter <= 0):
            self.ready_to_explode()
    def ready_to_explode(self):
        sm.sound_effect.play(SE_BOMB)
        gw.field_array[self.gx+1][self.gy+1] &= \
            MAX_BITS - FIELD_DICT['bomb']
        if(self.option == GENERAL_BOMB):
            self.explode()
        elif(self.option == CROSS_BOMB):
            self.explode_cross()
        elif(self.option == ICE_BOMB):
            self.explode_ice()
        elif(self.option == ICE_CROSS_BOMB):
            self.explode_ice_cross()
        elif(self.option == MINE_BOMB):
            self.explode_mine()
        gw.remove_object(self)
    def explode(self):
        for x in range(0, 15):
            sv.explosion.append(Explosion(x, self.gy, self.damage))
            gw.addleft_object(sv.explosion[-1], 'explode')
        for y in range(0, 9):
            sv.explosion.append(Explosion(self.gx, y, self.damage))
            gw.addleft_object(sv.explosion[-1], 'explode')
        self.x = -65535
    def explode_mine(self):
        for x in range(-1, 2):
            for y in range(-1, 2):
                gw.addleft_object(\
                    Explosion(self.gx+1+x, self.gy+1+y, self.damage), 'explode')

    def explode_cross(self):
        for i in range(0, 9, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy+i < 9): break
            gw.field_array[self.gx+i+1][self.gy+i+1] |= FIELD_DICT['explode']
            gw.addleft_object(Explosion(self.gx+i+1, \
                self.gy+i+1, self.damage), 'explode')
        for i in range(1, 9, 1):
            if not(-1 < self.gx-i < 15 and -1 < self.gy+i < 9): break
            gw.field_array[self.gx-i+1][self.gy+i+1] |= FIELD_DICT['explode']
            gw.addleft_object(Explosion(self.gx-i+1, self.gy+i+1, \
                self.damage), 'explode')
        for i in range(1, 9, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy-i < 9): break
            gw.field_array[self.gx+i+1][self.gy-i+1] |= FIELD_DICT['explode']
            gw.addleft_object(Explosion(self.gx+i+1, self.gy-i+1, \
                self.damage), 'explode')
        for i in range(1, 9, 1):
            if not(-1 < self.gx-i < 15 and -1 < self.gy-i < 9): break
            gw.field_array[self.gx-i+1][self.gy-i+1] |= FIELD_DICT['explode']
            gw.addleft_object(Explosion(self.gx-i+1, self.gy-i+1, \
                self.damage), 'explode')
        self.x = -65535

    def explode_ice(self):
        for x in range(-3, 4, 1):
            if not(-1 < self.gx+x < 15): continue
            if gw.field_array[self.gx+x+1][self.gy+1] \
                & ICE_REMOVER: continue
            gw.add_object(Ice(self.gx+x+1, self.gy+1), 'breakable')
        for y in range(-3, 4, 1):
            if not(-1 < self.gy+y < 9): continue
            if gw.field_array[self.gx+1][self.gy+y+1] \
                & ICE_REMOVER: continue
            gw.add_object(Ice(self.gx+1, self.gy+1+y), 'breakable')

    def explode_ice_cross(self):
        for i in range(-2, 3, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy+i < 9): continue
            if gw.field_array[self.gx+i+1][self.gy+i+1] \
                & ICE_REMOVER: continue
            gw.add_object(Ice(self.gx+1+i, self.gy+1+i), 'breakable')
        for i in range(-2, 3, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy-i < 9): continue
            if gw.field_array[self.gx+i+1][self.gy-i+1] \
                & ICE_REMOVER: continue
            gw.add_object(Ice(self.gx+1+i, self.gy+1-i), 'breakable')

    def draw(self):
        if(self.counter > 0):
            self.bomb_draw_case()
            gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['bomb']

    def bomb_draw_case(self):
        cntnum = ceil(self.counter)
        drawing_pos = None
        if self.option == 0:
            drawing_pos = (60 * int(self.frame), 0, 60, 60, self.x, self.y)
        else:
            drawing_pos = (60 * int(self.frame), 60 * (cntnum-1), 60, 60, self.x, self.y)
        if(self.option == 0):
            Bomb.image[cntnum-1+self.owner].clip_draw(*drawing_pos)
        elif(self.option == 1):
            Bomb.image2.clip_draw(*drawing_pos)
        elif(self.option == 2):
            Bomb.image3.clip_draw(*drawing_pos)
        elif(self.option == 3):
            Bomb.image4.clip_draw(*drawing_pos)
        
    def handle_collision(self, other, group):
        if group == COL_PHEAD_BOMB:
            self.counter = -65536
        elif group == COL_EHEAD_BOMB:
            self.counter = -65536

    def delete_from_server(self):
        sv.bomb.remove(self)