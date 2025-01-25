import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def calculate_weighted_mean(neighbors_list, current_state, p=3, inverted=False, epsilon=0.001):
    if inverted:
        weights = [1 / (abs(neighbor - current_state)**p + epsilon) for neighbor in neighbors_list]
    else:
        weights = [abs(neighbor - current_state)**p for neighbor in neighbors_list]
    
    total_weight = sum(weights)
    if total_weight == 0:
        total_weight = 1  # Avoid division by zero
    
    normalized_weights = [w / total_weight for w in weights]
    # weighted_mean = sum(w * neighbor for w, neighbor in zip(normalized_weights, neighbors_list))
    
    # return weighted_mean

    # return weights
    return normalized_weights

# neighbors_list = [0.56, 0.72, 0.73, 0.44, 0.67, 0.66, 0.55, 0.5]
neighbors_list = np.arange(0, 1, 0.05)
current_state = 0.5

weighted_mean = calculate_weighted_mean(neighbors_list, current_state, p=2)
# future_state = weighted_mean - current_state


# print(future_state)

# sns.scatterplot(x = neighbors_list, y = calculate_weighted_mean(neighbors_list, current_state, p = 2))

# plt.show()
print(calculate_weighted_mean(neighbors_list, current_state, 2))