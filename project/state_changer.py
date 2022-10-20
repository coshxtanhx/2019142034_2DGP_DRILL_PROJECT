def state_changer_activated(module_str):
    next_module_str = module_str
    while(next_module_str != ''):
        current_module_str = next_module_str
        exec('import ' + next_module_str)
        eval(next_module_str).enters()
        next_module_str = eval(next_module_str).acts()
        eval(current_module_str).exits()