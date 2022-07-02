import time

import particle
import random
from plotly import graph_objects as go
import tkinter

random.seed(version=2)
max_coord_x = 1200
max_coord_y = 800

window = tkinter.Tk()
myCanvas = tkinter.Canvas(window, bg="white", height=800, width=1200)
myCanvas.pack()

def canvas_draw_pixel(item_array):
    for item in item_array:
        myCanvas.create_rectangle(item.x_pos, item.y_pos, item.x_pos, item.y_pos)
    # window.after(100, canvas_draw_pixel(item_array))

def value_rand(value):
    v = int(value * random.random())
    return v

def value_rand_float(value):
    sw = 0
    while sw == 0:
        sw = random.randrange(-1, 2)
    v = value * random.random() * sw
    return v


if __name__ == "__main__":
    particle_array = []
    for i in range(0, 1000):
        particle_array.append(particle.Particle())

    for item in particle_array:
        item.x_pos = value_rand(max_coord_x)
        item.y_pos = value_rand(max_coord_y)
        item.x_force = value_rand_float(1)
        item.y_force = value_rand_float(1)

    points = []

    # Draw dots on the canvas
    for i in range(0, 5000):
        for item in particle_array:
            item.move()

    window.after(1000, canvas_draw_pixel(particle_array))

    window.mainloop()


