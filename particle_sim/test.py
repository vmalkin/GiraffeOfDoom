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


def draw_pixel(x_pos, y_pos):
    mycanvas.create_rectangle(x_pos, y_pos, x_pos + 3, y_pos + 3, fill="green", width=0)


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
    for i in range(0, 50):
        particle_array.append(Particle(grid_x, grid_y))

    # create collision grid
    grid_collisions = create_blank_grid()

    # populate collision grid with particle positions
    for p in particle_array:
        grid_collisions[p.x_pos][p.y_pos] = px_active


    while True:
        # create collision grid
        grid_collisions = create_blank_grid()

        # move particles. Update collision grid
        for p in particle_array:
            p.move()
            grid_collisions[p.x_pos][p.y_pos] = px_active

        # test for collisions

        # Draw particles
        mycanvas.delete("all")
        for p in particle_array:
            draw_pixel(p.x_pos, p.y_pos)

        mywindow.update()
    mywindow.mainloop()