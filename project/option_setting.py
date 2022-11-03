from coordinates_module import *
from pico2d import *
from buttons_ui import Option_volume_button, Option_volume_line, Option_button

volumes = [128, 128]
volumes_before = [128, 128]

def change_volume_and_quit(i):
    global acting, next_module, next_module_option
    if(i == 0):
        volumes_before[0], volumes_before[1] = volumes[0], volumes[1]
    elif(i == 1):
        volumes[0], volumes[1] = volumes_before[0], volumes_before[1]
    acting = False
    next_module, next_module_option = 'lastest', 'resume'

def handle_events():
    global acting, next_module, next_module_option
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            acting = False
            next_module, next_module_option = '', None
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                acting = False
                next_module, next_module_option = 'lastest', 'resume'
        elif event.type == SDL_MOUSEMOTION:
            for i in range(2):
                volume_buttons[i].drag_move(event.x)
                volumes[i] = button_pos_to_volmume(volume_buttons[i].x)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                for i in range(2):
                    if(volume_buttons[i].isclicked(event.x, event.y)):
                        break
                    elif(volume_lines[i].isclicked(event.x, event.y)):
                        volume_buttons[i].x = clamp(256, event.x, 664)
                        volume_buttons[i].clicked = True
                        break
                    elif(option_buttons[i].isclicked(event.x, event.y)):
                        change_volume_and_quit(i)
                        break
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                for i in range(2): volume_buttons[i].clicked = False

def enters(option):
    global acting, next_module, next_module_option
    global img_ui, img_button, volume_buttons, volume_lines, option_buttons
    acting = True
    next_module = ''
    next_module_option = None
    img_ui = load_image('img/option_ui.png')
    img_button = load_image('img/option_button.png')
    volume_buttons = [Option_volume_button(volume_to_button_pos(volumes[i]), \
        UI_HEIGHT//2 + i * 90) for i in range(2)]
    volume_lines = [Option_volume_line(UI_HEIGHT//2 + i * 90) for i in range(2)]
    option_buttons = [Option_button(UI_WIDTH//2 + i) for i in (-135, 135)]

def exits():
    global acting, next_module, next_module_option
    global img_ui, img_button, img_bg, volume_buttons, volume_lines, option_buttons
    acting = None
    next_module = ''
    next_module_option = None
    img_ui = None
    img_button = None
    img_bg = None
    volume_buttons = None
    volume_lines = None
    option_buttons = None

def acts():
    global img_bg
    from state_changer import state_stack
    if(state_stack[-2] == 'game_menu'): img_bg = load_image('img/field_menu.png')
    elif(state_stack[-2] == 'title_menu'): img_bg = load_image('img/title_bg.png')
    while(acting):
        clear_canvas()
        img_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        img_ui.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
        for i in range(2): volume_buttons[i].draw()
        update_canvas()
        handle_events()
        delay(0.01)
    return next_module, next_module_option

acting = None
next_module = ''
next_module_option = None
img_ui = None
img_button = None
img_bg = None
volume_buttons = None
volume_lines = None
option_buttons = None