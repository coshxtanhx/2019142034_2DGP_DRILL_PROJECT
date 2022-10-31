from coordinates_module import UI_WIDTH, UI_HEIGHT, get_distance

class Title_button():
    def __init__(self, image, y):
        self.image = image
        self.x = UI_WIDTH//2
        self.y = y
        self.enabled = True
    def isclicked(self, x, y):
        if(self.enabled and self.x - 197 < x < self.x + 197 and \
            UI_HEIGHT - (self.y + 50) < y < UI_HEIGHT - (self.y - 50)):
            return True
        else:
            False
    def draw(self):
        self.image.draw(UI_WIDTH // 2, self.y)

class Game_menu_button():
    def __init__(self, x):
        self.x = x
        self.y = 330
        self.enabled = True
    def isclicked(self, x, y):
        if(get_distance(x, y, self.x, self.y) < 60):
            return True
        else:
            False