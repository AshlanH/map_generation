import numpy as np
import tkinter as tk
import random
import utilities

class Map:
    def __init__(self, row, col, cell_size, canva, root, simulation_num):
        self.row = row
        self.col = col
        self.cell_cize = cell_size
        self.canva = canva
        self.root = root
        self.generation = 0
        self.simulation_num = simulation_num
        self.grid = [[Tile(x, y) for x in range(col)] for y in range(row)]

    def generate_map(self):
        self.canva.delete("all")
        for row in self.grid:
            for each_tile in row:
                coor = each_tile.coordinate()
                if each_tile.state >= 0.4:
                    intensity = int(255 * each_tile.state)
                    color = f'#00a0{intensity:02x}'
                elif each_tile.state < 0.4:
                    intensity = int(255 * each_tile.state)
                    color = f'#00a0{intensity:02x}'
                    # color = 'white'
                self.canva.create_rectangle(
                    coor["origin_x"], coor["origin_y"],
                    coor["end_x"], coor["end_y"],
                    # fill = f'#0078{intensity:02x}',
                    # outline = f'#0078{intensity:02x}'
                    fill = color, outline = color
                )
                # self.canva.create_text(
                #     coor["origin_x"] + CELL_SIZE / 2, 
                #     coor["origin_y"] + CELL_SIZE / 2,
                #     text = round(each_tile.get_state(), 3)
                # )

        # LABEL                
        self.canva.create_text(
            90, 30, font = ("Helvetica" , 16), fill = 'black',
            text = "Current Generation: {}\nLandmass: {}".format(
                self.generation, 
                # round(sum(value == 1 for value in self.statistics()) / (TOTAL_ROW * TOTAL_COL), 5)
                0
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
                yield tile.get_state()

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = round(random.random(), 3)
        self.future_state = self.state
        self.index = str(self.y * TOTAL_COL + self.x + 1)

    # ESSENTIAL mapping coordinate onto the canva
    def coordinate(self):
        return {
            "origin_x" : self.x * CELL_SIZE + OFFSET,
            "origin_y" : self.y * CELL_SIZE + OFFSET,
            "end_x" : self.x * CELL_SIZE + CELL_SIZE,
            "end_y" : self.y * CELL_SIZE + CELL_SIZE,
        }

    def get_coor(self):
        return "[{},{}]".format(self.y, self.x)
    
    def get_state(self):
        return self.state
    
    # Caps value between 0 to 1
    def increment(self, increment_value):
        return max(0, min(self.state + increment_value, 1))

    def get_neighbors(self):
        neighbors = np.array([[-1, -1], [0, -1], [1, -1],[-1, 0], [1, 0],[-1, 1], [0, 1], [1, 1]])
        neighbors_list = []

        # Enter the value/state of all valid neighboring cells
        # for dx, dy in neighbors:
        #     if((TOTAL_COL > self.x + dx >= 0)) and ((TOTAL_ROW > self.y + dy >= 0)):
        #         neighbors_list.append((start_map.grid[self.y + dy][self.x + dx]).get_state())
        return np.array(neighbors_list)

    # Rules for cellular automata
    def rule_gen(self, neighbors_list):
        # MODEL1
        if float(neighbors_list.mean()) >= float(self.state):
            # self.future_state = self.increment(random.uniform(-0.15, 0.15))
            self.future_state = self.increment(neighbors_list.mean() / len(neighbors_list))
        else:
            # self.future_state = self.increment(random.uniform(-0.15, 0.15))
            self.future_state = self.increment(-(neighbors_list.mean() / len(neighbors_list)) * random.uniform(1.04, 1.12))

    def update_state(self):
        self.state = self.future_state

# CONSTANTS
TOTAL_ROW = 60
TOTAL_COL = 90
CELL_SIZE = 15
OFFSET = 0

root = tk.Tk()
root.title("2D Map - Cellular Automata")


canvas = tk.Canvas(root, width = TOTAL_COL * CELL_SIZE + OFFSET, height = TOTAL_ROW * CELL_SIZE + OFFSET)
canvas.pack()


start_map = Map(TOTAL_ROW, TOTAL_COL, CELL_SIZE, canvas, root, 100)

start_map.simulation()

# sample_neighbors = start_map.grid[4][6].get_neighbors()
# print(type(sample_neighbors.mean()))
# print(type(start_map.grid[4][6].state))

root.mainloop()