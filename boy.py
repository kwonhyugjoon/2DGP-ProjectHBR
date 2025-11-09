from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_c, SDLK_z, SDLK_x

from hpasoul import HpASoul
from sword import Sword
import game_world
import game_framework
from state_machine import StateMachine

def space_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE

def time_out(event):
    return event[0] == 'TIME_OUT'
def time_out_no(event):
    return event[0] == 'TIME_OUT_NO'

def collide(event):
    return event[0] == 'collide'

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
def x_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_x

PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 1m
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_ACTION_DASH = 6
GRAVITY = 9.8

class Jump:

    def __init__(self, boy):
        self.boy = boy
        self.yv = PIXEL_PER_METER
        self.frame = 0

    def enter(self, event):
        pass

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_DASH * 0.15 * game_framework.frame_time) % 5 + 1
        self.boy.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        self.yv -= GRAVITY * game_framework.frame_time


    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(int(self.boy.frame) * 128, 100, 100, 100, self.boy.x, self.boy.y)
        else:  # face_dir == -1:
            self.boy.image.clip_draw(int(self.boy.frame) * 128, 0, 100, 100, self.boy.x, self.boy.y)

class Dash:
    dash_time = -1
    frame = 0
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
        frame = 0

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_DASH * 0.15 * game_framework.frame_time) % 5 + 1
        if get_time() - self.dash_time < 0.15:
            self.boy.x += self.boy.face_dir * RUN_SPEED_PPS * game_framework.frame_time * 20
        else:
            if self.boy.move == False:
                self.dash_time = -1
                self.boy.state_machine.handle_state_event(('TIME_OUT_NO', None))
            else:
                self.dash_time = -1
                self.boy.state_machine.handle_state_event(('TIME_OUT', None))


    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(int(self.frame) * 128, 1408, 128, 128, self.boy.x, self.boy.y)
        else:  # face_dir == -1: # left
            self.boy.image.clip_composite_draw(int(self.frame) * 128, 1408, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)

class Run:
    frame = 0
    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        if right_down(event) or left_up(event):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(event) or right_up(event):
            self.boy.dir = self.boy.face_dir = -1
        self.boy.move = True

    def exit(self, event):
        if x_down(event):
            self.boy.swing_sword()
        frame = 0
        if z_down(event) and self.boy.jump == False:
            self.boy.jump = True
            self.boy.yv = PIXEL_PER_METER * 0.6

    def do(self):
        if self.boy.jump == True:
            self.frame = (self.frame + FRAMES_PER_ACTION * 0.3 * game_framework.frame_time) % 8
            self.boy.x += self.boy.dir * RUN_SPEED_PPS * game_framework.frame_time
            self.boy.y += self.boy.yv * game_framework.frame_time * PIXEL_PER_METER
            self.boy.yv -= GRAVITY * game_framework.frame_time
        else :
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
            self.boy.x += self.boy.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.boy.face_dir == 1 and self.boy.jump == False:
            self.boy.image.clip_draw(int(self.frame) * 128, 1920, 128, 128, self.boy.x, self.boy.y)
        elif self.boy.face_dir == -1 and self.boy.jump == False:
            self.boy.image.clip_composite_draw(int(self.frame) * 128, 1920, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)
        elif self.boy.face_dir == 1 and self.boy.jump == True:
            self.boy.image.clip_draw(int(self.frame) * 128, 768, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_composite_draw(int(self.frame) * 128, 768, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)

class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        self.boy.dir = 0
        self.boy.move = False

    def exit(self, event):
        if x_down(event):
            self.boy.swing_sword()
        if z_down(event) and self.boy.jump == False:
            self.boy.jump = True
            self.boy.yv = PIXEL_PER_METER * 0.6

    def do(self):
        if self.boy.jump == True:
            self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * 0.3 * game_framework.frame_time) % 8
            self.boy.y += self.boy.yv * game_framework.frame_time * PIXEL_PER_METER
            self.boy.yv -= GRAVITY * game_framework.frame_time
        else:
            self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * TIME_PER_ACTION * game_framework.frame_time) % 8

    def draw(self):
        if self.boy.face_dir == 1 and self.boy.jump == False:
            self.boy.image.clip_draw(int(self.boy.frame) * 128, 128, 128, 128, self.boy.x, self.boy.y)
        elif self.boy.face_dir == -1 and self.boy.jump == False:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 128, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)
        elif self.boy.face_dir == 1 and self.boy.jump == True:
            self.boy.image.clip_draw(int(self.boy.frame) * 128, 768, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 768, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 110
        self.frame = 0
        self.jump = False
        self.yv = 0
        self.face_dir = 1
        self.dir = 0
        self.hp = 5
        self.soul = 100
        self.move = False
        self.image = load_image('simplehollowknight.png')

        self.see_state()
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.DASH = Dash(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_up: self.RUN, left_up: self.RUN, right_down: self.RUN, left_down: self.RUN, c_down: self.DASH, x_down: self.IDLE, z_down: self.IDLE},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, c_down: self.DASH, x_down: self.RUN, z_down: self.RUN},
                self.DASH: {time_out_no: self.IDLE, time_out: self.RUN, right_down: self.DASH, left_down: self.DASH, right_up: self.DASH, left_up: self.DASH},
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))

    def swing_sword(self):
        sword = Sword(self.x, self.y, self.face_dir)
        game_world.add_object(sword)

    def see_state(self):
        hpasoul = HpASoul(self.hp, self.soul)
        game_world.add_object(hpasoul)

    def get_bb(self):
        return self.x - 64, self.y - 32, self.x + 64, self.y + 32

    def handle_collision(self, group, other):
        if group == 'boy:grass':
            self.jump = False
            self.yv = 0