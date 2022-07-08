import random

grid_x = 1200
grid_y = 800
particle_array_length = 10000

px_dead = 0
px_active = 1


class Particle:
    def __init__(self):
        self.pos_x = random.randrange(2, grid_x - 2)
        self.pos_y = random.randrange(2, grid_y - 2)
        self.move_x = 1
        self.move_y = 0

    def movement_x(self):
        return self.pos_x + self.move_x

    def movement_y(self):
        return self.pos_y + self.move_y


def create_blank_grid():
    #  CReate blank collisions grid
    grid = []
    for i in range(0, grid_x):
        row = []
        for j in range(0, grid_y):
            row.append(px_dead)
        grid.append(row)
    return grid


if __name__ == "__main__":
    # create array of particles
    particle_array = []
    for i in range(0, particle_array_length):
        particle_array.append(Particle())

    for items in particle_array:


    #     mywindow.update()
    # mywindow.mainloop()