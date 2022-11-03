from pico2d import *

KWD, KAD, KSD, KDD, KESCD, KMD, \
MM, MLD, MLU, \
QUIT, *_ = range(1, 30)

EVENT_DICT = {
    #(type, key, button)
    (SDL_KEYDOWN, SDLK_w, None): KWD,
    (SDL_KEYDOWN, SDLK_a, None): KAD,
    (SDL_KEYDOWN, SDLK_s, None): KSD,
    (SDL_KEYDOWN, SDLK_d, None): KDD,
    (SDL_KEYDOWN, SDLK_m, None): KMD,
    (SDL_KEYDOWN, SDLK_ESCAPE, None): KESCD,
    (SDL_MOUSEMOTION, None, None): MM,
    (SDL_MOUSEBUTTONDOWN, None, SDL_BUTTON_LEFT): MLD,
    (SDL_MOUSEBUTTONUP, None, SDL_BUTTON_LEFT): MLU,
    (SDL_QUIT, None, None): QUIT
}

def convert_event(event):
    event_tuple = (event.type, event.key, event.button)
    if(event_tuple in EVENT_DICT):
        return EVENT_DICT[event_tuple]
    else:
        False
    