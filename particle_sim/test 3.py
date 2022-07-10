import copy
import tkinter as tk
import random

grid_x = 400
grid_y = 400

mywindow = tk.Tk()
mywindow.title("New Window")
mycanvas = tk.Canvas(mywindow, background="black", height=grid_y, width=grid_x)
# mycanvas1 = tk.Canvas(mywindow, background="white", height=grid_y, width=grid_x)
mycanvas.pack()

px_dead = 0
px_active = 1


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
    mycanvas.create_rectangle(x_pos, y_pos, x_pos + 1, y_pos + 1, fill=colour, width=0)

def game_o_life(x, y, grid_display):
    count = 0
    if x >= 1:
        if x <= grid_x - 1:
            if y >= 1:
                if y <= grid_y - 1:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if grid_display[x + i][y + j] == 1:
                                count = count + 1
    return count


if __name__ == "__main__":
    # create grid of particles
    grid_temp = create_blank_grid()
    grid_display = create_blank_grid()

    for i in range(0, grid_x):
        for j in range(0, grid_y):
            k = random.randrange(0, 800)
            if k == 1:
                grid_display[i][j] = px_active


    while True:
        # Draw particles
        mycanvas.delete("all")
        grid_temp = create_blank_grid()

        for i in range(0, grid_x):
            for j in range(0, grid_y):
                neighbors = game_o_life(i, j, grid_display)
                if neighbors < 2:
                    grid_temp[i][j] = px_dead
                if neighbors >= 2 and neighbors <= 2:
                    grid_temp[i][j] = px_active
                if neighbors > 2:
                    grid_temp[i][j] = px_dead

        grid_display = copy.deepcopy(grid_temp)

        for i in range(0, grid_x):
            for j in range(0, grid_y):
                if grid_display[i][j] == px_dead:
                    draw_pixel(i, j, "black")
                if grid_display[i][j] == px_active:
                    draw_pixel(i, j, "green")

        mywindow.update()
    mywindow.mainloop()
