from pico2d import *
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.5)

TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Sword:
    image = None
    def __init__(self, x, y, face_dir):
        self.frame = 0
        if Sword.image == None:
            Sword.image = load_image('Attack.png')
        self.start_time = get_time()
        self.x, self.y = x + face_dir * 130, y - 20
        self.face_dir = face_dir

    def draw(self):
        if self.face_dir == -1:  # right
            self.image.clip_draw(int(self.frame) * 680, 0, 680, 137, self.x, self.y, 204, 50)
        else:  # face_dir == -1: # left
            self.image.clip_composite_draw(int(self.frame) * 680, 0, 680, 137, 0, 'h',self.x, self.y, 204, 50)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - self.start_time > 0.1:
            game_world.remove_object(self)

    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 102, self.y - 25, self.x + 2, self.y + 25
        else:
            return self.x - 2, self.y - 25, self.x + 102, self.y + 25