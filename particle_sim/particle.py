class Particle:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.x_force = 0
        self.y_force = 0

    def move(self):
        move_x = self.x_pos + self.x_force
        move_y = self.y_pos + self.y_force
        self.x_pos = move_x
        self.y_pos = move_y


