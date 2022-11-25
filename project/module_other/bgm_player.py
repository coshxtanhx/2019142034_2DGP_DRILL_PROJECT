from pico2d import *
import module_state.option_setting as os

class Game_bgm:
    def play(self):
        self.bgm.repeat_play()
    def stop(self):
        self.bgm.stop()
    def set_volume(self, v):
        self.bgm.set_volume(v)
    def update(self):
        self.set_volume(os.volumes[1])

class Stage_bgm(Game_bgm):
    stage_bgm = [None for _ in range(5)]
    def __init__(self, num_str):
        self.idx = int(num_str) - 1
        if Stage_bgm.stage_bgm[self.idx] == None:
            Stage_bgm.stage_bgm[self.idx] = \
                load_music('snd/stage' + num_str + '_bgm.mp3')
        self.bgm = Stage_bgm.stage_bgm[self.idx]
        self.play()

class Title_bgm(Game_bgm):
    title_bgm = None
    def __init__(self):
        if Title_bgm.title_bgm == None:
            Title_bgm.title_bgm = load_music('snd/title_bgm.mp3')
        self.bgm = Title_bgm.title_bgm
        self.play()


class Volume_check_sound:
    sound = None
    volume = None
    def __init__(self):
        if Volume_check_sound.sound == None:
            Volume_check_sound.sound = load_wav('snd/zrescue.wav')
            Volume_check_sound.volume = os.volumes[0]
    def update(self):
        if Volume_check_sound.volume != os.volumes[0]\
            and os.volume_buttons[0].clicked == False:
            Volume_check_sound.volume = os.volumes[0]
            self.sound.set_volume(Volume_check_sound.volume)
            self.play()
    def play(self):
        Volume_check_sound.sound.play()

bgm = None
volume_check_sound = None