import copy
import time
import tkinter as tk
import random

grid_x = 1200
grid_y = 600

mywindow = tk.Tk()
mywindow.title("New Window")
mycanvas = tk.Canvas(mywindow, background="black", height=grid_y, width=grid_x)
# mycanvas1 = tk.Canvas(mywindow, background="white", height=grid_y, width=grid_x)
mycanvas.pack()

px_dead = 0
px_active = 1
px_quantity = 500

class Particle:
    def __init__(self):
        self.visible = True
        self.colour = "orange"
        self.pos_x = random.randrange(0, grid_x)
        self.pos_y = random.randrange(0, grid_y)
        self.move_x = random.randrange(-6, 6)
        self.move_y = random.randrange(-6, 6)

    def draw_pixel(self):
        mycanvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x + 2, self.pos_y + 2, fill=self.colour, width=0)

    def movement_x(self):
        return self.pos_x + self.move_x

    def movement_y(self):
        return self.pos_y + self.move_y

    def am_i_visible(self):
        if self.pos_x > grid_x:
            self.visible == False
        if self.pos_x < 0:
            self.visible == False
        if self.pos_y > grid_y:
            self.visible == False
        if self.pos_y < 0:
            self.visible == False


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


if __name__ == "__main__":
    particles = []
    for i in range(0, px_quantity):
        particles.append(Particle())

    while True:
        time.sleep(0.05)
        clear_canvas()
        drawing_array = []
        print(len(drawing_array))
        for p in particles:
            p.am_i_visible()
            if p.visible == True:
                p.pos_x = p.movement_x()
                p.pos_y = p.movement_y()
                drawing_array.append(p)
                p.draw_pixel()

        particles = copy.deepcopy(drawing_array)
        mywindow.update()
    mywindow.mainloop()



