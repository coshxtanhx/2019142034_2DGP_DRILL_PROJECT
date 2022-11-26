from module_other.term_table import *
from module_other.coordinates_module import *
import module_other.game_world as gw
import module_other.server as sv

def collide(a, b):
    if get_distance(a.x, a.y, b.x, b.y) < 40:
        return True
    return False

def add_collision_pairs_pack():
    gw.add_collision_pairs(sv.player, sv.apple, COL_PLAYER_APPLE)
    gw.add_collision_pairs(sv.player, sv.ice, COL_PLAYER_ICE)
    gw.add_collision_pairs(sv.player, sv.bomb, COL_PLAYER_BOMB)
    gw.add_collision_pairs(sv.player, sv.skin_wall, COL_PLAYER_SKINWALL)
    gw.add_collision_pairs(sv.player, sv.mine, COL_PLAYER_MINE)
    gw.add_collision_pairs(sv.player, sv.enemy, COL_PLAYER_ENEMY)
    gw.add_collision_pairs(sv.player, sv.wall, COL_PLAYER_WALL)