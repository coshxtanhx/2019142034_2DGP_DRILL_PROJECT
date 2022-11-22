from pico2d import *
from module_other.coordinates_module import UI_HEIGHT, UI_WIDTH

MAX_PAGE = 6

class Book_page:
    image = [None for _ in range(MAX_PAGE)]
    page = 0
    def __init__(self):
        Book_page.page = 0
        Book_page.load_new_image()
    def change_page(option):
        Book_page.page = (Book_page.page + option * 2) % Book_page.MAX_PAGE
        Book_page.load_new_image()
    def load_new_image():
        if Book_page.image[Book_page.page] == None:
            for i in range(2):
                Book_page.image[Book_page.page + i] = load_image('img/help' \
                    + str(Book_page.page//2) + str(i) + '.png')
    def draw(self):
        gap = 195
        for i in range(2):
            self.image[Book_page.page+i].draw(\
                UI_WIDTH//2 + gap*2*i - gap, UI_HEIGHT//2)