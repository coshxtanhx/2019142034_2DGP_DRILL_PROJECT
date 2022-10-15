from pico2d import *
from coordinates_module import UI_HEIGHT, UI_WIDTH

img_title_bg = load_image('img/title_bg.png')
img_title = [load_image('img/title_'+str(i)+'.png') for i in range(2)]
img_title_text = load_image('img/title_text.png')

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_s:
                global acting
                acting = False
                import title_menu
            elif event.key == SDLK_ESCAPE:
                acting = False

acting = True
frame = 0

while(acting):
    clear_canvas()
    img_title_bg.draw(UI_WIDTH // 2, UI_HEIGHT // 2)
    img_title[0].draw(500, 520)
    img_title[1].draw(470, 400)
    if frame < 50: img_title_text.draw(UI_WIDTH // 2, UI_HEIGHT // 2 - 100)
    frame = (frame + 1) % 100
    update_canvas()
    handle_events()
    delay(0.01)