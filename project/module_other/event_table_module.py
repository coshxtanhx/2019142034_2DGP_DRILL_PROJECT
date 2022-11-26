from pico2d import *

KWD, KAD, KSD, KDD, KED, KESCD, KMD, \
MM, MLD, MLU, \
QUIT, *_ = range(1, 30)

EVENT_DICT = {
    #(type, key, button)
    (SDL_KEYDOWN, SDLK_w, None): KWD,
    (SDL_KEYDOWN, SDLK_a, None): KAD,
    (SDL_KEYDOWN, SDLK_s, None): KSD,
    (SDL_KEYDOWN, SDLK_d, None): KDD,
    (SDL_KEYDOWN, SDLK_e, None): KED,
    (SDL_KEYDOWN, SDLK_m, None): KMD,
    (SDL_KEYDOWN, SDLK_ESCAPE, None): KESCD,
    (SDL_MOUSEMOTION, None, None): MM,
    (SDL_MOUSEBUTTONDOWN, None, SDL_BUTTON_LEFT): MLD,
    (SDL_MOUSEBUTTONUP, None, SDL_BUTTON_LEFT): MLU,
    (SDL_QUIT, None, None): QUIT
}

EVENT_SNAKE_HANDLES = (KWD, KAD, KSD, KDD, KED)

def convert_event(raw_event):
    event_tuple = (raw_event.type, raw_event.key, raw_event.button)
    #print(event_tuple)
    if(event_tuple in EVENT_DICT):
        return EVENT_DICT[event_tuple]
    else:
        False
    