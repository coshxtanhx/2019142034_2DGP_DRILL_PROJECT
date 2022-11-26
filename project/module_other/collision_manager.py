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
import module_other.game_world as gw
import module_other.server as sv

def collide(a, b):
    if get_distance(a.x, a.y, b.x, b.y) < 40:
        return True
    return False

def add_collision_pairs_automatically(o, is_list=False):
    if is_list: ot = type(o[0])
    else: ot = type(o)
    if ot == Player_body:
        gw.add_collision_pairs(o, None, COL_PLAYER_APPLE)
        gw.add_collision_pairs(o, None, COL_PLAYER_ICE)
        gw.add_collision_pairs(o, None, COL_PLAYER_BOMB)
        gw.add_collision_pairs(o, None, COL_PLAYER_SKINWALL)
        gw.add_collision_pairs(o, None, COL_PLAYER_MINE)
        gw.add_collision_pairs(o, None, COL_PLAYER_ENEMY)
        gw.add_collision_pairs(o, None, COL_PLAYER_WALL)
        gw.add_collision_pairs(None, o, COL_EXPLOSION_PLAYER)
    elif ot == Enemy_body:
        gw.add_collision_pairs(o, None, COL_ENEMY_APPLE)
        gw.add_collision_pairs(o, None, COL_ENEMY_ICE)
        gw.add_collision_pairs(o, None, COL_ENEMY_BOMB)
        gw.add_collision_pairs(o, None, COL_ENEMY_SKINWALL)
        gw.add_collision_pairs(None, o, COL_PLAYER_ENEMY)
        gw.add_collision_pairs(None, o, COL_EXPLOSION_ENEMY)
    elif ot == Explosion:
        gw.add_collision_pairs(o, None, COL_EXPLOSION_ENEMY)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_PLAYER)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_APPLE)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_ICE)
        gw.add_collision_pairs(o, None, COL_EXPLOSION_SKINWALL)
    elif ot in (Poison_apple, Normal_apple):
        gw.add_collision_pairs(None, o, COL_EXPLOSION_APPLE)
        gw.add_collision_pairs(None, o, COL_ENEMY_APPLE)
        gw.add_collision_pairs(None, o, COL_PLAYER_APPLE)
    elif ot == Bomb:
        gw.add_collision_pairs(None, o, COL_ENEMY_BOMB)
        gw.add_collision_pairs(None, o, COL_PLAYER_BOMB)
    elif ot == Ice:
        gw.add_collision_pairs(None, o, COL_EXPLOSION_ICE)
        gw.add_collision_pairs(None, o, COL_PLAYER_ICE)
        gw.add_collision_pairs(None, o, COL_ENEMY_ICE)
    elif ot == Mine:
        gw.add_collision_pairs(None, o, COL_PLAYER_MINE)
    elif ot == Skin_wall:
        gw.add_collision_pairs(None, o, COL_PLAYER_SKINWALL)
        gw.add_collision_pairs(None, o, COL_ENEMY_SKINWALL)
        gw.add_collision_pairs(None, o, COL_EXPLOSION_SKINWALL)