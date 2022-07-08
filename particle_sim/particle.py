import random

class Particle:
    def __init__(self, canvas_width, canvas_height):
        self.visible = True
        self.colour = "green"
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.x_pos = random.randrange(2, canvas_width - 2)
        self.y_pos = random.randrange(2, canvas_height - 2)
        self.x_force = random.randrange(-4, 4)
        self.y_force = random.randrange(-4, 4)


    def move(self):
        x = self.x_pos + int(self.x_force)
        y = self.y_pos + int(self.y_force)

        self.x_pos = x
        self.y_pos = y

    def bounce_x(self):
        entropy = 0.99
        self.x_force = -1 * self.x_force * entropy

    def bounce_y(self):
        entropy = 0.99
        self.y_force = -1 * self.y_force * entropy
