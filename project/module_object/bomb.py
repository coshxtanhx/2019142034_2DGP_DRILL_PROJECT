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
            Bomb.image3 = load_image('img/bomb_ice_cross.png')
            Bomb.image4 = load_image('img/bomb_ice.png')
    def update(self):
        self.counter -= gf.elapsed_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * gf.elapsed_time) % 3
        if(self.counter <= 0):
            self.ready_to_explode()
    def ready_to_explode(self):
        if(self.option == GENERAL_BOMB):
            self.explode()
        elif(self.option == CROSS_BOMB):
            self.explode(cross = True)
        elif(self.option == ICE_BOMB):
            self.explode_ice()
        elif(self.option == ICE_CROSS_BOMB):
            self.explode_ice(cross = True)
        elif(self.option == MINE_BOMB):
            self.explode_mine()
        gw.remove_object(self)

    def explode(self, cross=False):
        sm.sound_effect.play(SE_BOMB)
        sv.explosion.append(Explosion(self.gx, self.gy, self.damage))
        gw.add_object(sv.explosion[-1], 'explode')
        if cross: signs = ((+1, +1), (-1, +1), (-1, -1), (+1, -1))
        else: signs = ((+1, 0), (-1, 0), (0, -1), (0, +1))
        for sign in signs:
            for i in range(1, 9):
                x = self.gx + i * sign[0]
                y = self.gy + i * sign[1]
                if (x not in range(0,15)) or (y not in range(0,9)):
                    break
                sv.explosion.append(Explosion(x, y, self.damage))
                gw.add_object(sv.explosion[-1], 'explode')

    def explode_ice(self, cross=False):
        sm.sound_effect.play(SE_BOMB)
        sv.ice.append(Ice(self.gx, self.gy))
        gw.add_object(sv.ice[-1], 'breakable')
        if cross: signs = ((+1, +1), (-1, +1), (-1, -1), (+1, -1))
        else: signs = ((+1, 0), (-1, 0), (0, -1), (0, +1))
        for sign in signs:
            for i in range(1, 3):
                x = self.gx + i * sign[0]
                y = self.gy + i * sign[1]
                if (x not in range(0,15)) or (y not in range(0,9)):
                    break
                sv.ice.append(Ice(x, y))
                gw.add_object(sv.ice[-1], 'breakable')


    def explode_mine(self):
        for x in range(-1, 2):
            for y in range(-1, 2):
                sv.explosion.append(Explosion(self.gx+x, self.gy+y, self.damage))
                gw.add_object(sv.explosion[-1], 'explode')

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