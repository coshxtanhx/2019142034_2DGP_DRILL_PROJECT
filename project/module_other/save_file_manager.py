import pickle
from module_other.term_table import *

def remove_save_data():
    save_file[IS_VALID_FILE] = False
    file = open('data/save_data.sav', 'wb')
    pickle.dump(save_file, file)
    file.close()

def save_cur_state():
    save_file[IS_VALID_FILE] = True
    file = open('data/save_data.sav', 'wb')
    pickle.dump(save_file, file)
    file.close()

def load_cur_state():
    global save_file
    try:
        file = open('data/save_data.sav', 'rb')
        save_file = pickle.load(file)
        if save_file[IS_VALID_FILE] == False: return LOAD_FAILURE
        return LOAD_SUCCESS
    except:
        return LOAD_FAILURE

save_file = {
    CUR_CHARACTER: GENERAL_SNAKE,
    CUR_STAGE: STAGE1,
    CUR_NUM_OF_STARS: 0,
    IS_VALID_FILE: False
}