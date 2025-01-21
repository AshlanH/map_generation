import numpy as np
import random
import tkinter as tk
import utilities
root = tk.Tk()
root.title("2D Map - Cellular Automata")


canvas = tk.Canvas(root, width = 800, height = 150)
canvas.pack()

start_color = (244, 164, 96)  # Light brown
end_color = (101, 67, 33)     # Dark brown

def get_colors(list):
    for elevation in list:
        # color = utilities.interpolate_color(elevation, start_color, end_color)
        color = utilities.interpolate_color(utilities.normalize(elevation, 0.4, 1), start_color, end_color)
        yield f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

# output = get_colors([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
scaled_output = get_colors([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

for i in range(0, 7):
    color_hex = next(scaled_output)
    canvas.create_rectangle(
        i * 80, 0,
        i * 80 + 80,80,
        fill = color_hex,
        outline = color_hex
    )

root.mainloop()