# AI
RANDOM, CIRCLE, SWEEP, APPLE_HUNTER, \
    BOMB_TOUCH, APPLE_DEFENDER, SMARTER, STALKER = range(8)

# Bomb type
GENERAL_BOMB, CROSS_BOMB, ICE_BOMB, ICE_CROSS_BOMB, MINE_BOMB = range(5)
PLAYER_OWNS, ENEMY_OWNS = 0, 5

# Character
GENERAL_SNAKE, POISON_APPLE_SNAKE, \
    MINE_SWEEPER_SNAKE, SKIN_SHEDDER_SNAKE = '1234'

# Collision pairs
COL_PLAYER_APPLE, COL_PLAYER_ENEMY, COL_PLAYER_ICE, COL_PLAYER_MINE, \
    COL_PLAYER_BOMB, COL_PLAYER_SKINWALL, COL_PLAYER_WALL, \
    COL_ENEMY_APPLE, COL_ENEMY_ICE, COL_ENEMY_BOMB, COL_ENEMY_SKINWALL, \
    COL_EXPLOSION_ENEMY, COL_EXPLOSION_PLAYER, COL_EXPLOSION_APPLE, \
    COL_EXPLOSION_ICE, COL_EXPLOSION_SKINWALL,\
    *_ = range(50)

# Direction
RIGHT, UP, LEFT, DOWN = range(4)

# Phase
PHASE = (None,) + tuple(range(3, -1, -1))

# Rank
RANK_A, RANK_B, RANK_C, RANK_D, RANK_E = '01234'

# Sound Effect
SE_BOMB = 'snd/ttafi200.wav'
SE_EAT = 'snd/eat.wav'
SE_CRASHED = 'snd/crashed.wav'

# Stage
STAGE1, STAGE2, STAGE3, STAGE4, ENDING = '12345'

# Victory/Defeat
VICTORY, DEFEAT, STILL_PLAYING = 1, -1, 0