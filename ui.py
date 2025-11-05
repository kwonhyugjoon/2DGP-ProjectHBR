from pico2d import *

class Ui:
    def __init__(self):
        self.outline_image = load_image('health_outline.png')


    def draw(self):
        self.outline_image.draw(110, 700)

    def update(self):
        pass
