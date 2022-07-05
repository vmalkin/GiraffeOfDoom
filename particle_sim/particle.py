import random

class Particle:
    def __init__(self, canvas, canvas_width, canvas_height):
        self.x_pos = random.randrange(0, canvas_width)
        self.y_pos = random.randrange(0, canvas_height)
        self.x_force = random.randrange(-4, 4)
        self.y_force = random.randrange(-4, 4)
        self.canvas = canvas
        self.image = canvas.create_rectangle(self.x_pos, self.y_pos,
                                             self.x_pos + 2, self.y_pos + 2,
                                  fill="green", width=0)

    def move(self):
        # coords = self.canvas.coords(self.image)
        # print(coords)
        self.canvas.move(self.image, self.x_force, self.y_force)



