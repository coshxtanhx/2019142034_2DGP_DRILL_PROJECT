import pickle
from module_other.term_table import *

class SaveFile:
    def __init__(self):
        self.cur_stage = STAGE1
        self.cur_character = GENERAL_SNAKE
        self.stars = 0