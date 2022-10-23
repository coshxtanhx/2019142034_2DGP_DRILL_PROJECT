from pico2d import *

img_field = load_image('img/field.png')
img_snake_blue_head = \
    [load_image('img/snake_blue_head_' + str(i) + '.png') for i in range(4)]
img_snake_blue_body = load_image('img/snake_blue_body.png')

img_snake_orange_head = \
    [load_image('img/snake_orange_head_' + str(i) + '.png') for i in range(4)]
img_snake_orange_body = load_image('img/snake_orange_body.png')

img_apple = load_image('img/apple.png')
img_explode = load_image('img/explode.png')
img_bomb = \
    [load_image('img/bomb_' + str(i) + '.png') for i in range(1, 6)]

img_hpbar = load_image('img/hp_bar0.png')