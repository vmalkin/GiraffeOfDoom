import tkinter as tk
import time
from particle import Particle

grid_x = 1200
grid_y = 800

mywindow = tk.Tk()
mywindow.title("New Window")
mycanvas = tk.Canvas(mywindow, background="black", height=grid_y, width=grid_x)
mycanvas.pack()

px_dead = 0
px_active = 1

def clear_canvas():
    mycanvas.delete("all")


def draw_pixel(x_pos, y_pos, colour):
    mycanvas.create_rectangle(x_pos, y_pos, x_pos + 2, y_pos + 2, fill=colour, width=0)


def create_blank_grid():
    grid = []
    for i in range(0, grid_x + 1):
        row = []
        for j in range(0, grid_y + 1):
            row.append(px_dead)
        grid.append(row)
    return grid


if __name__ == "__main__":
    # create array of particles
    particle_array = []
    for i in range(0, 2000):
        particle_array.append(Particle(grid_x, grid_y))

    # create collision grid
    grid_collisions = create_blank_grid()

    # populate collision grid with particle positions
    for p in particle_array:
        grid_collisions[p.x_pos][p.y_pos] = px_active



    while True:
        # create collision grid
        grid_collisions = create_blank_grid()

        for p in particle_array:
            try:
                grid_collisions[p.x_pos][p.y_pos] = px_active
            except:
                pass

        # test for collisions - boundaries
        for p in particle_array:
            xx = p.x_pos + p.x_force
            yy = p.y_pos + p.y_force
            if xx >= grid_x or xx <= 0:
                p.bounce_x()
                p.colour = "cyan"
            if yy >= grid_y or yy <= 0:
                p.bounce_y()
                p.colour = "cyan"

        # test for collisions - other particles
            if p.x_pos - 1 > 1:
                if p.x_pos + 1 <= grid_x:
                    if p.y_pos - 1 > 1:
                        if p.y_pos + 1 <= grid_y:
                            if grid_collisions[p.x_pos - 1][p.y_pos] == px_active or grid_collisions[p.x_pos + 1][p.y_pos] == px_active:
                                p.bounce_x()
                                p.colour = "red"

                            if grid_collisions[p.x_pos][p.y_pos - 1] == px_active or grid_collisions[p.x_pos][p.y_pos + 1] == px_active:
                                p.bounce_y()
                                p.colour = "red"

        # Move particles
        for p in particle_array:
            p.move()

        # Draw particles
        mycanvas.delete("all")
        for p in particle_array:
            if p.visible == True:
                draw_pixel(p.x_pos, p.y_pos, p.colour)

        mywindow.update()
    mywindow.mainloop()