import numpy as np
import tkinter as tk
import random
import utilities
import math

class Map:
    def __init__(self, row, col, cell_size, canva, root, simulation_num, annot = False):
        self.row = row
        self.col = col
        self.cell_cize = cell_size
        self.canva = canva
        self.root = root
        self.generation = 0
        self.annot = annot
        self.simulation_num = simulation_num
        self.grid = [[Tile(x, y) for x in range(col)] for y in range(row)]

    def generate_map(self):
        self.canva.delete("all")
        for row in self.grid:
            for each_tile in row:
                coor = each_tile.coordinate()
                self.canva.create_rectangle(
                    coor["origin_x"], coor["origin_y"],
                    coor["end_x"], coor["end_y"],
                    fill = coor['color'], outline = coor['color']
                )
                if self.annot == True:
                    self.canva.create_text(
                        coor["origin_x"] + CELL_SIZE / 2, 
                        coor["origin_y"] + CELL_SIZE / 2,
                        text = round(each_tile.get_state(), 3)
                    )

        # LABEL                
        self.canva.create_rectangle(
            0, canvas.winfo_reqheight() - 60, 
            self.canva.winfo_reqwidth(), self.canva.winfo_reqheight(),
            fill = '#dce6e8'
        )
        self.canva.create_text(
            100, self.canva.winfo_reqheight() - 35, font = ("Helvetica" , 16), fill = 'black',
            text = "Current Generation: {}\nLandmass: {}".format(
                self.generation, 
                round(sum(value == "Land" for value in self.statistics()) / (TOTAL_ROW * TOTAL_COL), 5)
                
                )
        )

    def cellular_automata(self):
        for row in self.grid:
            for each_tile in row:
                each_tile.rule_gen(each_tile.get_neighbors())
                each_tile.update_state()

    def simulation(self):
        """Generate a new random map and schedule the next generation."""
        if self.generation <= self.simulation_num:
            self.generate_map()  # Update the canvas
            self.cellular_automata()
            self.generation += 1
            self.root.after(100, self.simulation)  # Schedule the next update
        else:
            print("Simulation complete")

    def statistics(self):
        for row in self.grid:
            for tile in row:
                yield tile.get_type()

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = random.uniform(0, 1)
        self.future_state = self.state
        self.index = str(self.y * TOTAL_COL + self.x + 1)
        self.update_state()

    # ESSENTIAL mapping coordinate onto the canva
    def coordinate(self):
        return {
            "origin_x" : self.x * CELL_SIZE + OFFSET,
            "origin_y" : self.y * CELL_SIZE + OFFSET,
            "end_x" : self.x * CELL_SIZE + CELL_SIZE,
            "end_y" : self.y * CELL_SIZE + CELL_SIZE,
            "color" : self.color
        }

    def get_coor(self):
        return "[{},{}]".format(self.y, self.x)
    
    def get_state(self):
        return self.state
    
    def get_type(self):
        return self.type
    
    # Caps value between 0 to 1
    def increment(self, increment_value):
        return max(0, min(self.state + increment_value, 1))

    # MODEL 2
    def get_neighbors(self):
        neighbors = np.array([[-1, -1], [0, -1], [1, -1],[-1, 0], [1, 0],[-1, 1], [0, 1], [1, 1]])
        neighbors_list = []

        # Enter the value/state of all valid neighboring cells
        for dx, dy in neighbors:
            if((TOTAL_COL > self.x + dx >= 0)) and ((TOTAL_ROW > self.y + dy >= 0)):
                neighbors_list.append((start_map.grid[self.y + dy][self.x + dx]).get_state())
        return np.array(neighbors_list)

    # Rules for cellular automata
    def rule_gen(self, neighbors_list):
        mean_difference=  np.mean([neighbor - self.state for neighbor in neighbors_list])

        # Removes rogue land tiles toward the end of the generation
        if start_map.generation > start_map.simulation_num * .98:
            if np.mean(neighbors_list) < 0.4:
                self.future_state = np.mean(neighbors_list)
                return

        if self.state >= 0.85:
            # self.future_state = self.increment(math.exp(-5.5 * self.state) * (mean_difference) + np.random.uniform(0.005,0.0012))
            self.future_state = self.increment(math.exp(-5.5 * self.state) * (mean_difference) + np.random.uniform(0.005,0.008))
        elif 0.4 <= self.state < 0.85:
            self.future_state = self.increment(math.exp(-3 * self.state) * (mean_difference) + np.random.uniform(-0.005, 0.016))
            # self.future_state = self.increment(math.exp(-3 * self.state) * (mean_difference) + np.random.uniform(-0.003, 0.008))
        elif self.state < 0.4:
            # self.future_state = self.increment(math.exp(-3.5 * self.state) * (mean_difference) + np.random.uniform(-0.095, -0.045))
            self.future_state = self.increment(math.exp(-3.5 * self.state) * (mean_difference) + np.random.uniform(-0.095, -0.080))



    def update_state(self):
        self.state = self.future_state
        # Update Type based on state
        if self.state >= 0.4:
            self.type = "Land"
        elif self.state < 0.4:
            self.type = "Sea"

        land_start_color = (244, 164, 96)  # Light brown
        land_end_color = (101, 67, 33)     # Dark brown

        sea_start_color = (50, 130, 180)  # Light blue (Sky Blue)
        sea_end_color = (80, 170, 200)    
        
        # Update color parameter based on type
        if self.type == "Land":
            normalize_elevation = utilities.normalize(self.state, 0.4, 1.0)
            self.color = utilities.interpolate_color(normalize_elevation, land_start_color, land_end_color)
        elif self.type == "Sea":
            normalize_elevation = utilities.normalize(self.state, 0.0, 0.4)
            self.color = utilities.interpolate_color(normalize_elevation, sea_start_color, sea_end_color)

# CONSTANTS
# TOTAL_ROW = 25
# TOTAL_COL = 35
# CELL_SIZE = 50

TOTAL_ROW = 55
TOTAL_COL = 80
CELL_SIZE = 10

# TOTAL_ROW = 75
# TOTAL_COL = 130
# CELL_SIZE = 10
OFFSET = 0

root = tk.Tk()
root.title("2D Map - Cellular Automata")

canvas = tk.Canvas(
    root, 
    width = TOTAL_COL * CELL_SIZE + OFFSET, 
    height = TOTAL_ROW * CELL_SIZE + OFFSET + 60 ## Additional Offset for display panel
    )
canvas.pack()

print(canvas.winfo_reqheight())
print(canvas.winfo_reqwidth())
start_map = Map(TOTAL_ROW, TOTAL_COL, CELL_SIZE, canvas, root, 140, annot=False)

start_map.simulation()
root.mainloop()