import title, title_menu, snake_move, option_setting, game_menu

def state_enter(next_module_str, option):
    eval(next_module_str).enters(option)
    state_stack.append(next_module_str)
    print(next_module_str + ' entered')

def state_exit(current_module_str):
    eval(current_module_str).exits()
    state_stack.pop()
    print(current_module_str + ' exited')

def state_exit_all():
    for i in range(len(state_stack)-1, -1, -1):
        eval(state_stack[i]).exits()
        print(state_stack[i] + ' exited')
        state_stack.pop()

def state_changer_activate(start_module_str):
    option = None
    next_module_str = start_module_str
    while(next_module_str != ''):
        current_module_str = next_module_str
        if(option != 'resume'):
            state_enter(next_module_str, option)
        eval(next_module_str).acting = True
        next_module_str, option = eval(next_module_str).acts()
        if(option == 'exitall'):
            state_exit_all()
        elif(option != 'pause'):
            state_exit(current_module_str)
            
state_stack = []