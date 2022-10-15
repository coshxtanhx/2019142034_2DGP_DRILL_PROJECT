from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH

img_title_bg = load_image('img/title_bg.png')
img_menu_new = load_image('img/title_menu_newgame.png')
img_menu_load = load_image('img/title_menu_loadgame.png')
img_menu_quit = load_image('img/title_menu_quit.png')

def handle_events():
    global acting
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            acting = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                acting = False
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if (UI_WIDTH//2 - 197 < event.x < UI_WIDTH//2 + 197 and \
                    UI_HEIGHT - (520 + 50) < event.y < UI_HEIGHT - (520 - 50)):
                    acting = False
                    import snake_move

acting = True
frame = 0

while(acting):
    clear_canvas()
    img_title_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    img_menu_new.draw(UI_WIDTH // 2, 520)
    img_menu_load.draw(UI_WIDTH // 2, 370)
    img_menu_quit.draw(UI_WIDTH // 2, 220)
    update_canvas()
    handle_events()
    delay(0.01)