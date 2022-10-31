msc_vol = 128
eff_vol = 128

def enters(option):
    global acting, next_module
    acting = True
    next_module = ''
    print('option')

def exits():
    pass

def acts():
    return next_module, None

acting = None
next_module = ''