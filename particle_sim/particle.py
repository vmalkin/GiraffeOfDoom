import random

class Particle:
    def __init__(self, canvas_width, canvas_height):
        self.visible = True
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.x_pos = random.randrange(1, canvas_width)
        self.y_pos = random.randrange(1, canvas_height)
        self.x_force = random.randrange(-4, 4)
        self.y_force = random.randrange(-4, 4)

    def move(self):
        x = self.x_pos + self.x_force
        y = self.y_pos + self.y_force

        self.x_pos = x
        self.y_pos = y

    def bounce_x(self):
        self.x_force = -1 * self.x_force

    def bounce_y(self):
        self.y_force = -1 * self.y_force
