def state_changer_activate(start_module_str):
    option = None
    next_module_str = start_module_str
    while(next_module_str != ''):
        current_module_str = next_module_str
        exec('import ' + next_module_str)
        if(option != 'resume'):
            eval(next_module_str).enters(option)
            state_stack.append(next_module_str)
            print(next_module_str + ' entered')
        next_module_str, option = eval(next_module_str).acts()
        if(option == 'exitall'):
            for i in range(len(state_stack)-1, -1, -1):
                eval(state_stack[i]).exits()
                print(state_stack[i] + ' exited')
                state_stack.pop()
        elif(option != 'pause'):
            eval(current_module_str).exits()
            state_stack.pop()
            print(current_module_str + ' exited')

state_stack = []