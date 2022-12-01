from pico2d import *
from module_other.term_table import *
from collections import defaultdict
import module_state.option_setting as ops

class Game_bgm:
    def play(self):
        self.bgm.repeat_play()
    def stop(self):
        self.bgm.stop()
    def set_volume(self, v):
        self.bgm.set_volume(v)
    def update(self):
        self.set_volume(ops.volumes[1])

class Stage_bgm(Game_bgm):
    stage_bgm = [None for _ in range(5)]
    def __init__(self, num_str):
        self.idx = int(num_str) - 1
        if Stage_bgm.stage_bgm[self.idx] == None:
            Stage_bgm.stage_bgm[self.idx] = \
                load_music('snd/stage' + num_str + '_bgm.mp3')
        self.bgm = Stage_bgm.stage_bgm[self.idx]
        ops.load_volume_data()
        self.update()
        self.play()

class Title_bgm(Game_bgm):
    title_bgm = None
    def __init__(self):
        if Title_bgm.title_bgm == None:
            Title_bgm.title_bgm = load_music('snd/title_bgm.mp3')
        self.bgm = Title_bgm.title_bgm
        ops.load_volume_data()
        self.update()
        self.play()

class Volume_check_sound:
    sound = None
    volume = None
    def __init__(self):
        if Volume_check_sound.sound == None:
            Volume_check_sound.sound = load_wav('snd/zrescue.wav')
        Volume_check_sound.volume = ops.volumes[0]
    def update(self):
        if abs(Volume_check_sound.volume - ops.volumes[0]) > 1\
            and ops.volume_buttons[0].clicked == False:
            Volume_check_sound.volume = ops.volumes[0]
            self.sound.set_volume(Volume_check_sound.volume)
            self.play()
    def play(self):
        Volume_check_sound.sound.play()

class Sound_effect:
    se_dict = defaultdict(str)
    volume = None
    se_cnt = 0
    se_len = 8
    se = [None for _ in range(se_len)]
    def __init__(self):
        Sound_effect.volume = ops.volumes[0]
    def update(self):
        Sound_effect.volume = ops.volumes[0]
    def play(self, snd):
        if Sound_effect.se_dict[snd] == '':
            Sound_effect.se_dict[snd] = load_wav(snd)
        Sound_effect.se[Sound_effect.se_cnt] = Sound_effect.se_dict[snd]
        Sound_effect.se[Sound_effect.se_cnt].set_volume(Sound_effect.volume)
        Sound_effect.se[Sound_effect.se_cnt].play()
        Sound_effect.se_cnt = (Sound_effect.se_cnt + 1) % Sound_effect.se_len


bgm = None
volume_check_sound = None
sound_effect = None