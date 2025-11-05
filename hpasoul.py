from pico2d import *
import math

class HpASoul:
    bar = [0, 0, 0, 0, 0]

    def __init__(self, hp, soul):
        self.hp_image = load_image('hp_.png')
        self.soul_image = load_image('soulfull.png')
        self.hp = hp
        self.soul = soul

    def draw(self):
        self.hp_image.clip_composite_draw(HpASoul.bar[0], 0, 80, 71, math.pi / 2, '', 150, 730, 40, 35)
        self.hp_image.clip_composite_draw(HpASoul.bar[1], 0, 80, 71, math.pi / 2, '', 190, 730, 40, 35)
        self.hp_image.clip_composite_draw(HpASoul.bar[2], 0, 80, 71, math.pi / 2, '', 230, 730, 40, 35)
        self.hp_image.clip_composite_draw(HpASoul.bar[3], 0, 80, 71, math.pi / 2, '', 270, 730, 40, 35)
        self.hp_image.clip_composite_draw(HpASoul.bar[4], 0, 80, 71, math.pi / 2, '', 310, 730, 40, 35)
        self.soul_image.draw(83,689, 108,107)

    def update(self):
        HpASoul.bar = [233, 233, 233, 233, 233]
        for i in range(self.hp):
            HpASoul.bar[i] = 0
