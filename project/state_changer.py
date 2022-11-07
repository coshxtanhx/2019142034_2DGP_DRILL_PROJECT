from pico2d import close_canvas
import module_state.title
import module_state.title_menu
import module_state.snake_move
import module_state.option_setting
import module_state.game_menu
import module_state.select_char

def state_enter(next_module_str, option):
    eval('module_state.' + next_module_str).enters(option)
    state_stack.append(next_module_str)
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
    eval('module_state.' + next_module_str).acting = True
    return eval('module_state.' + next_module_str).acts()

def state_changer_activate(start_module_str):
    option = None
    next_module_str = start_module_str
    while(next_module_str != ''):
        current_module_str = next_module_str
        if(option != 'resume'):
            state_enter(next_module_str, option)
        next_module_str, option = state_act(next_module_str)
        if(option == 'exitall'):
            state_exit_all()
        elif(option != 'pause'):
            state_exit(current_module_str)
        if(next_module_str == 'lastest'):
            next_module_str = state_stack[-1]
    close_canvas()
            
state_stack = []