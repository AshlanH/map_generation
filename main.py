import tkinter as tk

def draw_2d_map(canvas, grid, cell_size):
    """
    Draws a 2D map on a Tkinter Canvas.

    Parameters:
        canvas (tk.Canvas): The canvas to draw on.
        grid (list of lists): 2D grid representing the map. 1 = filled, 0 = empty.
        cell_size (int): The size of each cell in pixels.
    """
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # color = "black" if grid[row][col] == 1 else "white"
            x0, y0 = col * cell_size, row * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            output_text = "{} , {}\nIndex: {}, {}".format(x0, y0, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="gray")
            canvas.create_text(x0 + (cell_size / 2), y0 + (cell_size / 2), text = output_text, fill = 'black')

# Initialize the Tkinter window
root = tk.Tk()
root.title("2D Map on Canvas")

# Grid dimensions and cell size
rows, cols = 8 , 8
cell_size = 150
grid = [[row * cols + col + 1 for col in range(cols)] for row in range(rows)]

# Create and pack the Canvas
canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
canvas.pack()

# Draw the 2D map
draw_2d_map(canvas, grid, cell_size)
for each in grid:
    print(each)
# Run the Tkinter main loop
root.mainloop()
