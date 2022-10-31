from coordinates_module import UI_WIDTH, UI_HEIGHT

class title_button():
    def __init__(self, image, y):
        self.image = image
        self.y = y
        self.enabled = True
    def isclicked(self, x, y):
        if(self.enabled and UI_WIDTH//2 - 197 < x < UI_WIDTH//2 + 197 and \
            UI_HEIGHT - (self.y + 50) < y < UI_HEIGHT - (self.y - 50)):
            return True
        else:
            False
    def draw(self):
        self.image.draw(UI_WIDTH // 2, self.y)