from pico2d import *

from ui import Ui
from boy import Boy
from grass import Grass
import game_world

import game_framework


boy = None

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global running

    running = True
    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_collision_pairs('boy:grass', None, grass)

    ui = Ui()
    game_world.add_object(ui, 0)

    boy = Boy()
    game_world.add_object(boy, 1)
    game_world.add_collision_pairs('boy:grass', boy, None)

def update():
    game_world.update()
    game_world.handle_collision()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

