from pico2d import *

class Stage_bgm:
    stage_bgm = [None for _ in range(5)]
    def __init__(self, num_str):
        self.idx = int(num_str) - 1
        Stage_bgm.stage_bgm[self.idx] = \
            load_music('snd/stage' + num_str + '_bgm.mp3')
        self.bgm = Stage_bgm.stage_bgm[self.idx]
        self.play()
    def play(self):
        self.bgm.repeat_play()
    def stop(self):
        self.bgm.stop()
    def set_volume(self, v):
        self.bgm.set_volume(v)

class Volume_check_sound:
    sound = None
    def __init__(self):
        if Volume_check_sound.sound == None:
            Volume_check_sound.sound = load_wav('snd/zrescue.wav')
    def set_volume_and_play(self, v):
        Volume_check_sound.sound.set_volume(v)
        Volume_check_sound.sound.play()

bgm = None
volume_check_sound = None