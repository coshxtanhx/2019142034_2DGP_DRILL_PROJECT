from pico2d import close_canvas, delay
import module_state.title
import module_state.title_menu
import module_state.snake_move
import module_state.option_setting
import module_state.game_menu
import module_state.select_char
import module_state.how_to_play
from time import time

def change_state(next_module_str, next_module_option_str, next_data = None):
    global running, next_module, next_module_option, data
    running = False
    next_module, next_module_option, data = \
        next_module_str, next_module_option_str, next_data

def get_previous_state():
    return state_stack[-2]

def state_enter(next_module_str, data):
    import game_world
    game_world.cur_world = next_module_str
    state_stack.append(next_module_str)
    eval('module_state.' + next_module_str).enters(data)
    print(next_module_str + ' entered')

def state_exit(current_module_str):
    eval('module_state.' + current_module_str).exits()
    state_stack.pop()
    print(current_module_str + ' exited')

def state_exit_all():
    for i in range(len(state_stack)-1, -1, -1):
        eval('module_state.' + state_stack[i]).exits()
        print(state_stack[i] + ' exited')
        state_stack.pop()

def state_act(next_module_str):
    import game_world
    game_world.cur_world = next_module_str
    global running, next_module, next_module_option, data
    running = True
    start_time = time()
    cur_module = eval('module_state.' + next_module_str)
    while(running):
        if(time() > start_time + 0.014):
            start_time += 0.014
            cur_module.handle_events()
            cur_module.draw_all()
            cur_module.update()
    return next_module, next_module_option, data


def state_changer_activate(start_module_str):
    option, data = None, None
    next_module_str = start_module_str
    while(next_module_str != ''):
        current_module_str = next_module_str
        if(option != 'resume'):
            state_enter(next_module_str, data)
        next_module_str, option, data = state_act(next_module_str)
        if(option == 'exitall'):
            state_exit_all()
        elif(option != 'pause'):
            state_exit(current_module_str)
        if(next_module_str == 'lastest'):
            next_module_str = state_stack[-1]
    close_canvas()
            
state_stack = []
running = False
next_module = None
next_module_option = None
data = None