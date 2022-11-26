from pico2d import *
import module_other.game_framework as gf

PIXEL_PER_MM = (1.0 / 1.6)  # 1 pixel 1.6 mm
MOVE_SPEED_MMPS = 100
MOVE_SPEED_PPS = (MOVE_SPEED_MMPS * PIXEL_PER_MM)

START_X = (-160, 300, 1160)
START_Y = 720
DEST_X = (290, 460, 630)
DEST_Y = 333
MAX_FRAME = 18

class Star():
    image = None
    queue = 0
    def __init__(self, num):
        self.num = num
        self.x = START_X[self.num]
        self.y = START_Y
        self.timer = 0
        self.frame = 0
        if Star.image == None:
            Star.image = load_image('img/clear_star_ui.png')
    def __del__(self):
        Star.queue = 0
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        if Star.queue != self.num:
            return
        if self.frame > MAX_FRAME:
            Star.queue += 1
            return
        self.x = int(START_X[self.num] + (DEST_X[self.num] - START_X[self.num]) \
            * (self.frame / MAX_FRAME))
        self.y = int(START_Y + (DEST_Y - START_Y) * (self.frame / MAX_FRAME))
        self.timer += gf.elapsed_time
        self.frame = int(self.timer / 0.014)