def state_changer_activate(module_str):
    option = None
    next_module_str = module_str
    while(next_module_str != ''):
        current_module_str = next_module_str
        exec('import ' + next_module_str)
        if(option != 'resume'): eval(next_module_str).enters(option)
        next_module_str, option = eval(next_module_str).acts()
        if(option != 'pause'): eval(current_module_str).exits()