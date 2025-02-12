import numpy as np
import matplotlib.pyplot as plt

print(np.random.uniform())

cur_landmass = 0.3
target_landmass = 0.7

print(0.3 if np.random.uniform() > (1 - (cur_landmass / target_landmass)) else 0.7)