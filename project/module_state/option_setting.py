from module_other.coordinates_module import *
from pico2d import *
from module_other.event_table_module import *
from module_object.ui.background import *
from module_object.ui.option import Option_ui
from module_object.ui.button.rect_button import *
from module_object.ui.button.circle_button import *
import module_other.game_framework as gf
import module_other.game_world as gw
import module_other.sound_manager as sm
import module_other.save_file_manager as sfm
from module_other.term_table import *

MAX_VOL = 128

volumes = {BGM: 64, SE: 64}

def change_volume(i):
    if(i == SAVE_CHANGES):
        sfm.save_vol_data()
        sm.bgm.set_volume(sfm.volume_data.vol_bgm)
    elif(i == DISCARD_CHANGES):
        sfm.volume_data.vol_se = volumes[SE]
        sfm.volume_data.vol_bgm = volumes[BGM]
        volumes[BGM] = sfm.volume_data.vol_bgm
        sm.bgm.set_volume(volumes[BGM])

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            gf.change_state('', None)
        elif event == KESCD:
            change_volume(1)
            gf.change_state('lastest', 'resume')
        elif event == MM:
            for i in range(2):
                if volume_buttons[i].clicked:
                    volume_buttons[i].drag_move(raw_event.x)
        elif event == MLD:
            for i in range(2):
                if(volume_buttons[i].isclicked(raw_event.x, raw_event.y)):
                    break
                elif(volume_lines[i].isclicked(raw_event.x, raw_event.y)):
                    volume_buttons[i].x = clamp(256, raw_event.x, 664)
                    volume_buttons[i].clicked = True
                    break
                elif(option_buttons[i].isclicked(raw_event.x, raw_event.y)):
                    change_volume(i)
                    gf.change_state('lastest', 'resume')
                    break
        elif event == MLU:
            for i in range(2):
                volume_buttons[i].clicked = False

def enter():
    global img_bg, img_ui, volume_buttons, volume_lines, option_buttons
    sfm.load_vol_data()
    volumes[SE] = sfm.volume_data.vol_se
    volumes[BGM] = sfm.volume_data.vol_bgm
    sm.volume_check_sound = sm.Volume_check_sound()
    img_ui = Option_ui()
    volume_buttons = [Option_volume_button(volume_to_button_pos(volumes[i]), \
        UI_HEIGHT//2 + i * 90) for i in range(2)]
    volume_lines = [Option_volume_line(UI_HEIGHT//2 + i * 90) for i in range(2)]
    option_buttons = [Option_button(UI_WIDTH//2 + i) for i in (-135, 135)]

    previous_state = gf.get_previous_state()
    if(previous_state == 'game_menu'):
        img_bg = Background('menu')
    elif(previous_state == 'title_menu'):
        img_bg = Background('main')

    gw.add_object(img_bg, 0)
    gw.add_object(img_ui, 1)
    gw.add_objects(volume_buttons, 2)

def exit():
    global img_ui, img_button, img_bg, volume_buttons, volume_lines, option_buttons
    img_ui = None
    img_button = None
    img_bg = None
    volume_buttons = None
    volume_lines = None
    option_buttons = None
    gw.clear_world()

def draw_all():
    clear_canvas()
    img_bg.draw()
    for objs in gw.all_objects():
        objs.draw()
    update_canvas()

def update():
    sfm.volume_data.vol_se = button_pos_to_volume(volume_buttons[0].x)
    sfm.volume_data.vol_bgm = button_pos_to_volume(volume_buttons[1].x)
    sm.bgm.update()
    sm.volume_check_sound.update()
    sm.sound_effect.update()

img_ui = None
img_button = None
img_bg = None
volume_buttons = None
volume_lines = None
option_buttons = None