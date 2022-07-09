import random
import time
import tkinter as tk

grid_x = 1200
grid_y = 800
particle_array_length = 5000

mywindow = tk.Tk()
mywindow.title("New Window")
mycanvas = tk.Canvas(mywindow, background="black", height=grid_y, width=grid_x)
# mycanvas1 = tk.Canvas(mywindow, background="white", height=grid_y, width=grid_x)
mycanvas.pack()

px_dead = 0
px_active = 1


class Particle:
    def __init__(self):
        self.visible = True
        self.colour = "green"
        self.pos_x = random.randrange(500, 700)
        self.pos_y = random.randrange(300, 500)
        self.move_x = random.randrange(-6, 6)
        self.move_y = random.randrange(-6, 6)

    def movement_x(self):
        return self.pos_x + self.move_x

    def movement_y(self):
        return self.pos_y + self.move_y

    def bounce_x(self):
        self.move_x = -1 * self.move_x

    def bounce_y(self):
        self.move_y = -1 * self.move_y


def create_blank_grid():
    #  CReate blank collisions grid
    grid = []
    for i in range(0, grid_x + 1):
        row = []
        for j in range(0, grid_y + 1):
            row.append(px_dead)
        grid.append(row)

    return grid


def clear_canvas():
    mycanvas.delete("all")


def draw_pixel(x_pos, y_pos, colour):
    mycanvas.create_rectangle(x_pos, y_pos, x_pos + 2, y_pos + 2, fill=colour, width=0)


if __name__ == "__main__":
    # create array of particles
    particle_array = []
    for i in range(0, particle_array_length):
        particle_array.append(Particle())

    while True:
        # time.sleep(0.05)
        # Test to see if movement results in boundary violations, if so, bounce
        for p in particle_array:
            if p.movement_x() > grid_x:
                p.visible == False
            if p.movement_x() < 0:
                p.visible == False
            if p.movement_y() > grid_y:
                p.visible == False
            if p.movement_y() < 0:
                p.visible == False

        # Test for collisions between particles
        # current locations of particles
        grid_collision = create_blank_grid()
        for p in particle_array:
            if p.visible == True:
                grid_collision[p.pos_x][p.pos_y] = px_active
        # see if movement for particle causes collision, if so, bounce
        for p in particle_array:
            if grid_collision[p.movement_x()][p.movement_y()] == px_active:
                p.bounce_x()
                p.bounce_y()

        # move particles
        for p in particle_array:
            if p.visible == True:
                p.pos_x = p.movement_x()
                p.pos_y = p.movement_y()

        # Draw particles
        mycanvas.delete("all")
        for p in particle_array:
            draw_pixel(p.pos_x, p.pos_y, p.colour)
        mywindow.update()
    mywindow.mainloop()