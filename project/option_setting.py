from state_changer import state_stack

msc_vol = 128
eff_vol = 128

def enters(option):
    global acting, next_module, next_module_option
    acting = True
    next_module = 'game_menu'
    next_module_option = 'resume'

def exits():
    pass

def acts():
    return state_stack[-2], 'resume'

acting = None
next_module = ''
next_module_option = None