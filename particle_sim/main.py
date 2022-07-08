import tkinter as tk
import time
from particle import Particle

canvas_width = 1200
canvas_height = 800
mywindow = tk.Tk()
mywindow.title("New Window")
mycanvas = tk.Canvas(mywindow, background="black",
                     height=canvas_height, width=canvas_width)
mycanvas.pack()

grid_display = []

for i in range(0, 100):
    grid_display.append(Particle(mycanvas, canvas_width, canvas_height))

while True:
    for p in grid_display:
        p.move()
        if p.x_pos >= canvas_width or p.x_pos <= 0:
            p.bounce_x()
        if p.y_pos >= canvas_height or p.y_pos <= 0:
            p.bounce_y()
        p.draw()
    time.sleep(0.1)
    mywindow.update()

mywindow.mainloop()
