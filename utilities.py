

# Regulates increment of values between 0 to 1
def increment(self, increment_value):
        return max(0, min(self.state + increment_value, 1))

def normalize(value, min_range, max_range):
    return(value - min_range )/(max_range - min_range)

def interpolate_color(elevation, start_color, end_color):
    """Interpolate between two RGB colors based on elevation (0.0 to 1.0)."""
    return tuple(
        int(start + (end - start) * elevation)
        for start, end in zip(start_color, end_color)
    )