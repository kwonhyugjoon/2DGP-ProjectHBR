from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_c, SDLK_z

import game_world
import game_framework
from state_machine import StateMachine

def space_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE

def time_out(event):
    return event[0] == 'TIME_OUT'
def time_out_no(event):
    return event[0] == 'TIME_OUT_NO'

def right_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT
def right_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT
def left_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT
def left_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT

def c_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_c
def z_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_z

PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 1m
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Jump:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        if z_down(event):
            pass

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)


class Dash:
    dash_time = -1

    def __init__(self, boy):
        self.boy = boy


    def enter(self, event):
        if self.dash_time == -1:
            self.dash_time = get_time()

        if right_down(event) or left_down(event) or right_up(event) or left_up(event):
            if self.boy.move == False:
                self.boy.move = True
            else:
                self.boy.move = False

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - self.dash_time < 0.1:
            self.boy.x += self.boy.face_dir * RUN_SPEED_PPS * game_framework.frame_time * 30
        else:
            if self.boy.move == False:
                self.dash_time = -1
                self.boy.state_machine.handle_state_event(('TIME_OUT_NO', None))
            else:
                self.dash_time = -1
                self.boy.state_machine.handle_state_event(('TIME_OUT', None))


    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else:  # face_dir == -1: # left
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Run:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        if right_down(event) or left_up(event):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(event) or right_up(event):
            self.boy.dir = self.boy.face_dir = -1
        self.boy.move = True

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.boy.x += self.boy.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        self.boy.dir = 0
        self.boy.move = False

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 200, 100, 100, self.boy.x, self.boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.move = False
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.DASH = Dash(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_up: self.RUN, left_up: self.RUN, right_down: self.RUN, left_down: self.RUN, c_down: self.DASH},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, c_down: self.DASH},
                self.JUMP: {},
                self.DASH: {time_out_no: self.IDLE, time_out: self.RUN, right_down: self.DASH, left_down: self.DASH, right_up: self.DASH, left_up: self.DASH}
            }
        )

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))
