from pico2d import *

class Stage_bgm():
    stage_bgm = [None for _ in range(5)]
    def __init__(self, num):
        self.idx = num - 1
        Stage_bgm.stage_bgm[self.idx] = \
            load_music('snd/stage' + str(num) + '_bgm.mp3')
        self.bgm = Stage_bgm.stage_bgm[self.idx]
        self.plays()
    def plays(self):
        self.bgm.repeat_play()
    def stops(self):
        print(45355)
        self.bgm.stop()