import numpy as np
import tkinter as tk
import random
import time

class Map:
    def __init__(self, row, col, cell_size, canva, root):
        self.row = row
        self.col = col
        self.cell_cize = cell_size
        self.canva = canva
        self.root = root
        self.generation = 0
        self.grid = [[Tile(x, y) for x in range(col)] for y in range(row)]

    def generate_map(self):
        self.canva.delete("all")
        for row in self.grid:
            for each_tile in row:
                coor = each_tile.coordinate()
                color = {
                    0 : "#4585d9",
                    1 : "#51ad50"
                    # 0 : "#51ad50",
                    # 1 : "#4585d9"
                }

                self.canva.create_rectangle(
                    coor["origin_x"], coor["origin_y"],
                    coor["end_x"], coor["end_y"],
                    fill = color[each_tile.get_state()], 
                    outline = color[each_tile.get_state()]
                )
        self.canva.create_text(
            90, 30, font = ("Helvetica" , 16), fill = 'black',
            text = "Current Generation: {}\nLandmass:{}".format(
                self.generation, 
                round(sum(value == 1 for value in self.statistics()) / (TOTAL_ROW * TOTAL_COL), 5)
                )
        )

    def cellular_automata(self):
        for row in self.grid:
            for each_tile in row:
                each_tile.rule_gen(each_tile.get_neighbors())
                each_tile.update_state()

    def generate_new_map(self):
        """Generate a new random map and schedule the next generation."""
        if self.generation < 38:
            self.generate_map()  # Update the canvas
            self.cellular_automata()
            self.generation += 1
            self.root.after(10, self.generate_new_map)  # Schedule the next update
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
        self.state = random.choices([0, 1], weights = [1, 4]).pop()
        self.future_state = None
        self.index = str(self.y * TOTAL_COL + self.x + 1)

    # mapping coordinate onto the canva
    def coordinate(self):
        return {
            "origin_x" : self.x * CELL_SIZE + OFFSET,
            "origin_y" : self.y * CELL_SIZE + OFFSET,
            "end_x" : self.x * CELL_SIZE + CELL_SIZE,
            "end_y" : self.y * CELL_SIZE + CELL_SIZE,
        }

    def __repr__(self):
        return self.index

    def get_coor(self):
        return "[{},{}]".format(self.y, self.x)
    
    def get_state(self):
        return self.state
    
    def get_neighbors(self):
        neighbors = np.array([
            [-1, -1], [0, -1], [1, -1],
            [-1, 0], [1, 0],
            [-1, 1], [0, 1], [1, 1]
            ])
        neighbors_list = []

        for dx, dy in neighbors:
            # print(self.y + dy, self.x + dx)
            if((TOTAL_COL > self.x + dx >= 0)) and ((TOTAL_ROW > self.y + dy >= 0)):
                neighbors_list.append((start_map.grid[self.y + dy][self.x + dx]).get_state())
            else:
                neighbors_list.append(None)
        return neighbors_list


    # Rules for cellular automata
    def rule_gen(self, neighbors_list):
        # MODEL1
        # if neighbors_list.count(1) >= 7:
        #     self.future_state = 1
        # elif 3 <= neighbors_list.count(1) < 7:
        #     gen_value = 1 if random.random() < 0.58 else 0
        #     self.future_state = gen_value
        # elif  neighbors_list.count(1) < 3:
        #     self.future_state = 0

        #  MODEL 2
        fixed_rand = random.random()
        if neighbors_list.count(1) == 8:
            self.future_state = 1
        elif neighbors_list.count(1) == 7:
            self.future_state = 1
        elif neighbors_list.count(1) == 6:
            self.future_state = 1 if fixed_rand < .63 else 0
        elif neighbors_list.count(1) == 5:
            self.future_state = 1 if fixed_rand < .53 else 0
        elif neighbors_list.count(1) == 4:
            self.future_state = 1 if fixed_rand < .54 else 0
        elif neighbors_list.count(1) == 3:
            self.future_state = 1 if fixed_rand < .5 else 0
        elif neighbors_list.count(1) == 2:
            self.future_state = 1 if fixed_rand < .1675 else 0
        elif neighbors_list.count(1) == 1:
            self.future_state = 0
        elif neighbors_list.count(1) == 0:
            self.future_state = 0


    def update_state(self):
        self.state = self.future_state

# CONSTANTS
TOTAL_ROW = 140
TOTAL_COL = 200
CELL_SIZE = 7.5
# TOTAL_ROW = 75
# TOTAL_COL = 110
# CELL_SIZE = 15
OFFSET = 0

root = tk.Tk()
root.title("2D Map - Cellular Automata")


canvas = tk.Canvas(root, width = TOTAL_COL * CELL_SIZE + OFFSET, height = TOTAL_ROW * CELL_SIZE + OFFSET)
canvas.pack()


start_map = Map(TOTAL_ROW, TOTAL_COL, CELL_SIZE, canvas, root)
# for row in start_map.grid:
#     grid_list = []
#     for each_tile in row:
#         grid_list.append(each_tile.get_state())
#     print(grid_list)
# for i in range(4):
#     start_map.cellular_automata()
# print(' ')

# start_map.cellular_automata()
# root.after(1000, start_map.generate_map)

start_map.generate_new_map()


root.mainloop()