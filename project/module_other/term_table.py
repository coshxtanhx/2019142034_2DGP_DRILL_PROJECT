# AI
RANDOM, CIRCLE, SWEEP, APPLE_HUNTER, \
    BOMB_TOUCH, APPLE_DEFENDER, SMARTER, STALKER = range(8)

# Bomb type
BOMB_TYPES = range(4)
GENERAL_BOMB, CROSS_BOMB, ICE_CROSS_BOMB, ICE_BOMB, MINE_BOMB = range(5)
PLAYER_OWNS, ENEMY_OWNS = 0, 5

# Character
GENERAL_SNAKE, POISON_APPLE_SNAKE, \
    MINE_SWEEPER_SNAKE, SKIN_SHEDDER_SNAKE = '1234'

# Collision pairs
COL_PHEAD_APPLE, COL_PLAYER_EHEAD, COL_PLAYER_ICE, COL_PHEAD_MINE, \
    COL_PHEAD_BOMB, COL_PHEAD_SKINWALL, COL_PHEAD_WALL, COL_PHEAD_ENEMY, \
    COL_EHEAD_APPLE, COL_ENEMY_ICE, COL_EHEAD_BOMB, COL_EHEAD_SKINWALL, \
    COL_EXPLOSION_ENEMY, COL_EXPLOSION_PLAYER, COL_EXPLOSION_APPLE, \
    COL_EXPLOSION_ICE, COL_EXPLOSION_SKINWALL, COL_APPLE_SKINWALL,\
    COL_APPLE_ICE, \
    *_ = range(50)

# Direction
RIGHT, UP, LEFT, DOWN = range(4)

# Phase
PHASES = range(1,5)
PHASE1, PHASE2, PHASE3, PHASE4 = PHASES

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