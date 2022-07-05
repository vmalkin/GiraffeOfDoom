import tkinter as tk

canvas_width = 1200
canvas_height = 800

window = tk.Tk()
mycanvas = tk.Canvas(window, height=canvas_height, width=canvas_width)
window.title("New Window")


window.mainloop()