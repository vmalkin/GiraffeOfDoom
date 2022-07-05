import tkinter as tk
import time

canvas_width = 800
canvas_height = 800
mywindow = tk.Tk()
mywindow.title("New Window")
mycanvas = tk.Canvas(mywindow, background="white",
                     height=canvas_height, width=canvas_width)
mycanvas.grid()

for i in range(0, 200):
    mycanvas.create_rectangle(100 + i, 100 + i, 100 + i, 100 + i,
                              fill="green", width=0)
    time.sleep(0.01)
    mywindow.update()

mywindow.mainloop()
