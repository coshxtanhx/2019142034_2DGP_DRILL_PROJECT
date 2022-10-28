from pico2d import *

img_field = load_image('img/field.png')
img_snake_blue_head = \
    [load_image('img/snake_blue_head_' + str(i) + '.png') for i in range(4)]
img_snake_blue_body = load_image('img/snake_blue_body.png')

img_snake_orange_head = \
    [load_image('img/snake_orange_head_' + str(i) + '.png') for i in range(4)]
img_snake_orange_body = load_image('img/snake_orange_body.png')