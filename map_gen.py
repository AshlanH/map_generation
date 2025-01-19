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
                }

                self.canva.create_rectangle(
                    coor["origin_x"], coor["origin_y"],
                    coor["end_x"], coor["end_y"],
                    fill = color[each_tile.get_state()], 
                    # outline = "#1f1c15"
                )
                # self.canva.create_text(
                #     coor["origin_x"] + (C ELL_SIZE / 2), 
                #     coor["origin_y"]  + (CELL_SIZE / 2),
                #     text = each_tile.get_coor(), anchor = 'center'
                # )        
        self.canva.create_rectangle(
            10, 10,
            150, 30,
            fill = "white", outline = 'black'
            )
        self.canva.create_text(
            80, 20, text = "Current Generation: {}\nLandmass:{}".format(
                self.generation, sum(value == 0 for value in self.statistics())
                )
        )

    def cellular_automata(self):
        for row in self.grid:
            for each_tile in row:
                each_tile.rule_gen(each_tile.get_neighbors())
                each_tile.update_state()

    def generate_new_map(self):
        """Generate a new random map and schedule the next generation."""
        if self.generation < 35:
            self.generate_map()  # Update the canvas
            self.cellular_automata()
            self.generation += 1
            print(self.statistics())
            self.root.after(50, self.generate_new_map)  # Schedule the next update
        else:
            print("Simulation complete")

    def statistics(self):
        for row in self.grid:
            for tile in row:
                yield tile

        

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
        if neighbors_list.count(1) >= 7:
            # gen_value = 1 if random.random() < 0.8 else 0
            # self.future_state = gen_value
            self.future_state = 1
        elif 3 <= neighbors_list.count(1) < 7:
            gen_value = 1 if random.random() < 0.58 else 0
            self.future_state = gen_value
        elif  neighbors_list.count(1) < 3:
            self.future_state = 0
            # gen_value = 1 if random.random() < 0.2 else 0
            # self.future_state = gen_value

    def update_state(self):
        self.state = self.future_state

# CONSTANTS
TOTAL_ROW = 135
TOTAL_COL = 180
CELL_SIZE = 10
OFFSET = 1.5

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