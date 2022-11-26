from module_other.term_table import *
from module_other.coordinates_module import *
from module_object.apple import *
from module_object.ice import *
from module_object.snake_enemy import *
from module_object.snake_player import *
from module_object.skin_wall import *
from module_object.bomb import *
from module_object.explosion import *
from module_object.mine import *
from module_object.wall import *
import module_other.game_world as gw
import module_other.server as sv

def collide(a, b):
    if type(a) in (Player,):
        return collide_with_snake_body(a, b)
    if type(b) in (Player,):
        return collide_with_snake_body(b, a)
    return (get_distance(a.x, a.y, b.x, b.y) < 40)

def collide_with_snake_body(snake, o):
    for i in range(0, snake.length, LENGTH_PER_GRID):
        if get_distance(*snake.bodies_pos[i], o.x, o.y) < 40:
            return True
    return False

def add_collision_pairs_automatically(o, is_list=False):
    if is_list: ot = type(o[0])
    else: ot = type(o)
    if ot == Player:
        gw.add_collision_pairs(o, None, COL_PLAYER_ICE)
        gw.add_collision_pairs(None, o, COL_EXPLOSION_PLAYER)
        gw.add_collision_pairs(o, None, COL_PLAYER_EHEAD)
    if ot == Player_head:
        gw.add_collision_pairs(o, None, COL_PHEAD_APPLE)
        gw.add_collision_pairs(o, None, COL_PHEAD_BOMB)
        gw.add_collision_pairs(o, None, COL_PHEAD_SKINWALL)
        gw.add_collision_pairs(o, None, COL_PHEAD_MINE)
        gw.add_collision_pairs(o, None, COL_PHEAD_ENEMY)
        gw.add_collision_pairs(o, None, COL_PHEAD_WALL)
    elif ot == Enemy_body:
        gw.add_collision_pairs(o, None, COL_EHEAD_APPLE)
        gw.add_collision_pairs(o, None, COL_ENEMY_ICE)
        gw.add_collision_pairs(o, None, COL_EHEAD_BOMB)
        gw.add_collision_pairs(o, None, COL_EHEAD_SKINWALL)
        gw.add_collision_pairs(None, o, COL_PLAYER_EHEAD)
        gw.add_collision_pairs(None, o, COL_EXPLOSION_ENEMY)
        gw.add_collision_pairs(None, o, COL_PHEAD_ENEMY)
    elif ot == Explosion:
        gw.add_collision_pairs(o, None, COL_EXPLOSION_ENEMY)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_PLAYER)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_APPLE)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_ICE)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_SKINWALL)
    elif ot in (Poison_apple, Normal_apple):
        gw.add_collision_pairs(None, o, COL_EXPLOSION_APPLE)
        gw.add_collision_pairs(None, o, COL_EHEAD_APPLE)
        gw.add_collision_pairs(None, o, COL_PHEAD_APPLE)
    elif ot == Bomb:
        gw.add_collision_pairs(None, o, COL_EHEAD_BOMB)
        gw.add_collision_pairs(None, o, COL_PHEAD_BOMB)
    elif ot == Ice:
        gw.add_collision_pairs(None, o, COL_EXPLOSION_ICE)
        gw.add_collision_pairs(None, o, COL_PLAYER_ICE)
        gw.add_collision_pairs(None, o, COL_ENEMY_ICE)
    elif ot == Mine:
        gw.add_collision_pairs(None, o, COL_PHEAD_MINE)
    elif ot == Skin_wall:
        gw.add_collision_pairs(None, o, COL_PHEAD_SKINWALL)
        gw.add_collision_pairs(None, o, COL_EHEAD_SKINWALL)
        gw.add_collision_pairs(None, o, COL_EXPLOSION_SKINWALL)
    elif ot == Wall:
        gw.add_collision_pairs(None, o, COL_PHEAD_WALL)