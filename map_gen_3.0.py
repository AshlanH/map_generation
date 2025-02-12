import numpy as np
import tkinter as tk
import random
import utilities
import math
import scipy.ndimage as ndimage

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
            150, self.canva.winfo_reqheight() - 35, font = ("Helvetica" , 16), fill = 'black',
            text = "Current Generation: {} | Progress: {}%\nLandmass: {}".format(
                self.generation, 
                round((self.generation / self.simulation_num) * 100, 3),
                round(sum(value == "Land" for value in self.statistics()) / (TOTAL_ROW * TOTAL_COL), 5)
                )
        )

    def simulation(self): # **MAIN** Starts Simulation
        """Generate a new random map and schedule the next generation."""
        cur_landmass = round(sum(value == "Land" for value in self.statistics()) / (TOTAL_ROW * TOTAL_COL), 5)
        if self.generation <= self.simulation_num - 1: # generation rule at 0 - 90% of simulation
            for row in self.grid:
                for each_tile in row:
                    each_tile.formation(self.generation, self.simulation_num)
                    each_tile.update_state()
            self.generation += 1 # raise pass
            self.generate_map() # update canvas
            self.root.after(100, self.simulation)  # next pass

        else: #At final pass, equalize the border
            for row in self.grid:
                for each_tile in row:
                    each_tile.equalize()
                    each_tile.update_state()
            self.generate_map() # update canvas
            self.canva.create_text(
                500, self.canva.winfo_reqheight() - 35, font = ("Helvetica" , 16), fill = 'black',
                text = "Simulation Complete"
            )

    def statistics(self):
        for row in self.grid:
            for tile in row:
                yield tile.get_type()

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = random.choices([0, 1], weights = [1, 2]).pop()
        self.future_state = self.state
        self.index = str(self.y * TOTAL_COL + self.x + 1)
        self.update_state()
        self.age = 0

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
        # return max(0, min(self.state + increment_value, 1))
        self.future_state = max(0, min(self.state + increment_value, 1))

    # MODEL 2
    def get_neighbors(self, eight_way = True):
        if eight_way: neighbors = np.array([[-1, -1], [0, -1], [1, -1],[-1, 0], [1, 0],[-1, 1], [0, 1], [1, 1]])
        else: neighbors = np.array([[0, -1], [-1, 0], [1, 0], [0, 1]])
        neighbors_list = []

        # Enter the value/state of all valid neighboring cells
        for dx, dy in neighbors:
            if((TOTAL_COL > self.x + dx >= 0)) and ((TOTAL_ROW > self.y + dy >= 0)):
                neighbors_list.append((start_map.grid[self.y + dy][self.x + dx]))
        return np.array(neighbors_list)

    # Rules for formation | Pass current landmass as criteria
    def formation(self, generation, simulation_num):
        alpha = 1.3
        neighbors_list = self.get_neighbors()
        neighbor_mean = np.mean([a.get_state() for a in neighbors_list])
        # mean_difference =  np.mean([neighbor.get_state() - self.state for neighbor in neighbors_list])
        land_neighbor =  sum(neighbor.get_type() == 'Land' for neighbor in neighbors_list)

        fixed_rand = random.random()
        match land_neighbor:
            case 8:
                self.age += 1
                if self.age < simulation_num * 0.65:
                    self.future_state = neighbor_mean + np.random.uniform(0.00, 0.001)
                else:
                    self.future_state = np.clip(neighbor_mean + (alpha * np.random.uniform(0.002, 0.01)), 0, 1)
            case 7:
                self.future_state = neighbor_mean
            case 6:
                self.future_state = 0.65 if fixed_rand < .65 else 0.3
            case 5:
                self.future_state = 0.6 if fixed_rand < .55 else 0.2
            case 4:
                self.future_state = 0.575 if fixed_rand < .54 else 0.2
            case 3:
                self.future_state = 0.5 if fixed_rand < .5 else 0.2
            case 2:
                self.future_state = 0.5 if fixed_rand < .175 else 0.3
            case 1:
                if self.type != "Sea": self.future_state = 0.3
                else: self.increment(np.random.uniform(-0.015, -0.01))
            case 0:
                if self.type != "Sea": self.future_state = 0.3
                else: self.increment(np.random.uniform(-0.034, -0.03))


    ## ADDITIONAL FUNCTIONS
    def smooth_slopes(self, beta=0.1):
            diff_sum = sum(a.get_state() for a in self.get_neighbors(eight_way = False))
            self.increment(beta * diff_sum / 4)  # Balance slope

    def equalize(self): #Toward the end, pass a blur over the map to smooth out borders
        neighbors_list = self.get_neighbors()
        neighbor_mean = np.mean([a.get_state() for a in neighbors_list])
        self.future_state = neighbor_mean

    def update_state(self):
        self.state = self.future_state
        # Update Type based on state
        if self.state >= 0.4:
            self.type = "Land"
        elif self.state < 0.4:
            self.type = "Sea"

        land_start_color = (244, 164, 96)  # Light brown
        land_end_color = (101, 67, 33)     # Dark brown
        sea_start_color = (50, 130, 180)  # Light blue
        sea_end_color = (80, 170, 200) # Dark blue
        forest_start_color = (144, 238, 144) # Light green
        forest_end_color = (34, 139, 34) # Dark green
        
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

# TOTAL_ROW = 60
# TOTAL_COL = 85
# CELL_SIZE = 10

TOTAL_ROW = 70
TOTAL_COL = 200
CELL_SIZE = 4.5
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
start_map = Map(TOTAL_ROW, TOTAL_COL, CELL_SIZE, canvas, root, 35, annot=False)

start_map.simulation()

root.mainloop()