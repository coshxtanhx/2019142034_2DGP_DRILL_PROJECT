from collections import deque

def clear_server():
    global bg, player, player_head, enemy, enemy_head, bomb, \
        apple, hp_bar, explosion, ice, mine, cloud, broken, \
            skin_wall, wall, screen_off, fragment, mine_field
    bg = None
    player = None
    player_head = None
    enemy = None
    enemy_head = None
    bomb = deque()
    apple = None
    hp_bar = None
    explosion = []
    ice = []
    mine = []
    mine_field = []
    cloud = None
    broken = []
    skin_wall = []
    wall = []
    screen_off = None
    fragment = []

bg = None
player = None
player_head = None
enemy = None
enemy_head = None
bomb = deque()
apple = None
hp_bar = None
explosion = []
ice = []
mine = []
mine_field = []
cloud = None
broken = []
skin_wall = []
wall = []
screen_off = None
fragment = []