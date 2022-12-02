import pickle
from module_other.term_table import *
from module_object.snake_player import LENGTH_PER_GRID

class SaveFile:
    def __init__(self, character = GENERAL_SNAKE):
        self.is_valid_file = False
        self.cur_character = character
        self.cur_stage = STAGE1
        self.number_of_stars = 0

class EndState:
    def __init__(self, character, stage, length):
        self.charcter = character
        self.stage = stage
        self.length = length
    def get_star_num(self):
        le = self.length // LENGTH_PER_GRID + 1
        if le >= 6: return 3
        if le >= 4: return 2
        return 1

def remove_save_data():
    save_file.is_valid_file = False
    file = open('data/save_data.sav', 'wb')
    pickle.dump(save_file, file)
    file.close()

def save_cur_state():
    save_file.cur_stage = end_state.stage
    save_file.cur_character = end_state.charcter
    save_file.number_of_stars = end_state.get_star_num()
    save_file.is_valid_file = True
    file = open('data/save_data.sav', 'wb')
    pickle.dump(save_file, file)
    file.close()

def load_cur_state():
    global save_file
    try:
        file = open('data/save_data.sav', 'rb')
        save_file = pickle.load(file)
        if save_file.is_valid_file == False: return LOAD_FAILURE
        return LOAD_SUCCESS
    except:
        return LOAD_FAILURE

save_file = SaveFile()
end_state = EndState(None, None, None)