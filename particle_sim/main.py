import tkinter as tk
import time
from particle import Particle

canvas_width = 800
canvas_height = 800
mywindow = tk.Tk()
mywindow.title("New Window")
mycanvas = tk.Canvas(mywindow, background="black",
                     height=canvas_height, width=canvas_width)
mycanvas.pack()


particles = []
for i in range(0, 1000):
    particles.append(Particle(mycanvas, canvas_width, canvas_height))

while True:
    # time.sleep(0.005)
    for p in particles:
        p.move()
        mywindow.update()

mywindow.mainloop()
