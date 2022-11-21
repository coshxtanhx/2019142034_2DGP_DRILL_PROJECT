from module_other.coordinates_module import *
from pico2d import *
from collections import deque
import module_other.game_world as gw

ice_removing_obj = FIELD_DICT['enemy'] + FIELD_DICT['explode'] \
    + FIELD_DICT['bomb'] + FIELD_DICT['apple'] + FIELD_DICT['ice']

def bomb_draw_case(option, is_enemy, count, x, y):
    cntnum = ceil(count / 70)
    if(option == 0):
        bomb.image[cntnum-1+is_enemy].clip_draw(60 * (count % 3), 0, 60, 60, x, y)
    elif(option == 1):
        bomb.image2.clip_draw(60 * (count % 3), 60 * (cntnum-1), 60, 60, x, y)
    elif(option == 2):
        bomb.image3.clip_draw(60 * (count % 3), 60 * (cntnum-1), 60, 60, x, y)
    elif(option == 3):
        bomb.image4.clip_draw(60 * (count % 3), 60 * (cntnum-1), 60, 60, x, y)

class Skin:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.frame = 700
        if(Skin.image == None):
            Skin.image = load_image('img/snake_skinwall.png')
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
            import module_object.snake_player_obj
            module_object.snake_player_obj.Blue_body.get_damaged()
        if cur_loc & (FIELD_DICT['head'] + FIELD_DICT['enemy'] \
            + FIELD_DICT['explode']):
            gw.remove_object(self)

class Ice:
    image = None
    def __init__(self, gx, gy):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.frame = 700
        if(Ice.image == None):
            Ice.image = load_image('img/ice.png')
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
        cur_loc = gw.field_array[self.gx][self.gy]
        if cur_loc & (FIELD_DICT['player']):
            import module_object.snake_player_obj
            module_object.snake_player_obj.Blue_body.get_damaged()
        if cur_loc & (FIELD_DICT['player'] + FIELD_DICT['enemy'] \
            + FIELD_DICT['explode']):
            gw.remove_object(self)


class explosion:
    image = None
    def __init__(self, gx, gy, damage):
        self.gx, self.gy = gx, gy
        self.x, self.y = grid_to_coordinates(self.gx-1, self.gy-1)
        self.frame = 6
        self.damage = damage
        if(explosion.image == None):
            explosion.image = load_image('img/explode.png')
    def draw(self):
        self.image.clip_draw(60 * (self.frame // 2), 0, 60, 60, self.x, self.y)
    def update(self):
        self.frame -= 1
        if self.frame <= 0:
            gw.remove_object(self)
    def check_col(self):
        if self.frame != 3:
            return
        cur_loc = gw.field_array[self.gx][self.gy]
        if cur_loc & (FIELD_DICT['enemy']):
            import module_object.snake_enemy_obj as se
            se.Enemy_body.get_damaged(self.damage)
        if cur_loc & (FIELD_DICT['player']):
            import module_object.snake_player_obj as sp
            sp.Blue_body.get_damaged()
            

class bomb:
    explode_snd = None
    image = None
    image2 = None
    image3 = None
    image4 = None
    def __init__(self, x, y, damage, option = 0):
        self.gx, self.gy = coordinates_to_grid(x, y)
        self.x, self.y = grid_to_coordinates(self.gx, self.gy)
        self.counter = 350 if (option != 4) else 1
        self.damage = damage
        self.option = option
        self.is_enemy = 5 if (self.damage == 0) else 0
        if bomb.explode_snd == None:
            bomb.explode_snd = load_wav('snd/ttafi200.wav')
        if bomb.image == None:
            bomb.image = \
                [load_image('img/bomb_' + str(i) + '.png') for i in range(1, 11)]
            bomb.image2 = load_image('img/bomb_cross.png')
            bomb.image3 = load_image('img/bomb_ice.png')
            bomb.image4 = load_image('img/bomb_ice_cross.png')
    def update(self):
        self.counter -= 1
        if(self.counter == 0 or self.counter <= -65535):
            self.ready_to_explode()
    def ready_to_explode(self):
        bomb.explode_snd.play()
        gw.field_array[self.gx+1][self.gy+1] &= \
            MAX_BITS - FIELD_DICT['bomb']
        if(self.option == 0):
            self.explode()
        elif(self.option == 1):
            self.explode_cross()
        elif(self.option == 2):
            self.explode_ice()
        elif(self.option == 3):
            self.explode_ice_cross()
        elif(self.option == 4):
            self.explode_mine()
        gw.remove_object(self)
    def explode(self):
        for x in range(self.gx+1, 0, -1):
            gw.field_array[x][self.gy+1] |= FIELD_DICT['explode']
            gw.addleft_object(\
                explosion(x, self.gy+1, self.damage), 'explode')
        for x in range(self.gx+1, 16, +1):
            gw.field_array[x][self.gy+1] |= FIELD_DICT['explode']
            gw.addleft_object(\
                explosion(x, self.gy+1, self.damage), 'explode')
        for y in range(self.gy+1, 10, +1):
            gw.field_array[self.gx+1][y] |= FIELD_DICT['explode']
            gw.addleft_object(\
                explosion(self.gx+1, y, self.damage), 'explode')
        for y in range(self.gy+1, 0, -1):
            gw.field_array[self.gx+1][y] |= FIELD_DICT['explode']
            gw.addleft_object(\
                explosion(self.gx+1, y, self.damage), 'explode')
        self.x = -65535
    def explode_mine(self):
        for x in range(-1, 2):
            for y in range(-1, 2):
                gw.addleft_object(\
                    explosion(self.gx+1+x, self.gy+1+y, self.damage), 'explode')


    def explode_cross(self):
        for i in range(0, 9, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy+i < 9): break
            gw.field_array[self.gx+i+1][self.gy+i+1] |= FIELD_DICT['explode']
            gw.addleft_object(explosion(self.gx+i+1, \
                self.gy+i+1, self.damage), 'explode')
        for i in range(1, 9, 1):
            if not(-1 < self.gx-i < 15 and -1 < self.gy+i < 9): break
            gw.field_array[self.gx-i+1][self.gy+i+1] |= FIELD_DICT['explode']
            gw.addleft_object(explosion(self.gx-i+1, self.gy+i+1, \
                self.damage), 'explode')
        for i in range(1, 9, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy-i < 9): break
            gw.field_array[self.gx+i+1][self.gy-i+1] |= FIELD_DICT['explode']
            gw.addleft_object(explosion(self.gx+i+1, self.gy-i+1, \
                self.damage), 'explode')
        for i in range(1, 9, 1):
            if not(-1 < self.gx-i < 15 and -1 < self.gy-i < 9): break
            gw.field_array[self.gx-i+1][self.gy-i+1] |= FIELD_DICT['explode']
            gw.addleft_object(explosion(self.gx-i+1, self.gy-i+1, \
                self.damage), 'explode')
        self.x = -65535

    def explode_ice(self):
        for x in range(-3, 4, 1):
            if not(-1 < self.gx+x < 15): continue
            if gw.field_array[self.gx+x+1][self.gy+1] \
                & ice_removing_obj: continue
            gw.add_object(Ice(self.gx+x+1, self.gy+1), 'ice')
        for y in range(-3, 4, 1):
            if not(-1 < self.gy+y < 9): continue
            if gw.field_array[self.gx+1][self.gy+y+1] \
                & ice_removing_obj: continue
            gw.add_object(Ice(self.gx+1, self.gy+1+y), 'ice')

    def explode_ice_cross(self):
        for i in range(-2, 3, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy+i < 9): continue
            if gw.field_array[self.gx+i+1][self.gy+i+1] \
                & ice_removing_obj: continue
            gw.add_object(Ice(self.gx+1+i, self.gy+1+i), 'ice')
        for i in range(-2, 3, 1):
            if not(-1 < self.gx+i < 15 and -1 < self.gy-i < 9): continue
            if gw.field_array[self.gx+i+1][self.gy-i+1] \
                & ice_removing_obj: continue
            gw.add_object(Ice(self.gx+1+i, self.gy+1-i), 'ice')

    def draw(self):
        if(self.counter > 0):
            bomb_draw_case(self.option, self.is_enemy, self.counter, self.x, self.y)
            gw.field_array[self.gx+1][self.gy+1] |= FIELD_DICT['bomb']
        
    def check_col(self):
        cur_loc = gw.field_array[self.gx+1][self.gy+1]
        if cur_loc & (FIELD_DICT['head'] + FIELD_DICT['ehead']):
            self.counter = -65536