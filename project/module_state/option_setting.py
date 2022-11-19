from module_other.coordinates_module import *
from pico2d import *
from module_other.event_table_module import *
from module_object.background_obj import *
from module_object.buttons_obj \
    import Option_volume_button, Option_volume_line, Option_button
import module_other.state_changer as sc
import module_other.game_world as gw

MAX_VOL = 128

volumes = [64, 64]
volumes_before = [64, 64]

def load_volume_data():
    try:
        file = open('datas/savevolume.txt', 'r')
        volume_str = file.read(7)
        file.close()
        volume_read = [int(data) for data in volume_str.split()]
        if not(0 <= volume_read[0] <= MAX_VOL and 0 <= volume_read[1] <= MAX_VOL):
            1/0
        volumes[0], volumes[1] = volume_read[0], volume_read[1]
    except:
        volumes[0], volumes[1] = 64, 64
        volumes[0], volumes[1] = 64, 64


def change_volume(i):
    if(i == 0):
        volumes_before[0], volumes_before[1] = volumes[0], volumes[1]
        file = open('datas/savevolume.txt', 'w')
        file.write(str(volumes[0]) + ' ' + str(volumes[1]))
        file.close()
    elif(i == 1):
        volumes[0], volumes[1] = volumes_before[0], volumes_before[1]

def handle_events():
    events = get_events()
    for raw_event in events:
        event = convert_event(raw_event)
        if event == QUIT:
            sc.change_state('', None)
        elif event == KESCD:
            change_volume(1)
            sc.change_state('lastest', 'resume')
        elif event == MM:
            for i in range(2):
                volume_buttons[i].drag_move(raw_event.x)
                volumes[i] = button_pos_to_volume(volume_buttons[i].x)
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
                    sc.change_state('lastest', 'resume')
                    break
        elif event == MLU:
            for i in range(2): volume_buttons[i].clicked = False

def enters(option):
    global img_bg
    global img_ui, volume_buttons, volume_lines, option_buttons
    load_volume_data()
    img_ui = Option_ui()
    volume_buttons = [Option_volume_button(volume_to_button_pos(volumes[i]), \
        UI_HEIGHT//2 + i * 90) for i in range(2)]
    volume_lines = [Option_volume_line(UI_HEIGHT//2 + i * 90) for i in range(2)]
    option_buttons = [Option_button(UI_WIDTH//2 + i) for i in (-135, 135)]

    previous_state = sc.get_previous_state()
    if(previous_state == 'game_menu'):
        img_bg = Background('menu')
    elif(previous_state == 'title_menu'):
        img_bg = Background('main')

    gw.add_object(img_bg, 0)
    gw.add_object(img_ui, 1)
    gw.add_objects(volume_buttons, 2)

def exits():
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
    pass

img_ui = None
img_button = None
img_bg = None
volume_buttons = None
volume_lines = None
option_buttons = None