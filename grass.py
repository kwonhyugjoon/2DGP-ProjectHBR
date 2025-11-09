from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200,30)

    def update(self):
        pass

    def get_bb(self):
        return 0, 0, 1600, 70

    def handle_collision(self, group, other):
        if group == 'boy:grass':
            pass