

list = [
    [0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0]
    ]

def all_elements_2d(l): 
    for sublist in l:
        for element in sublist:
            yield element


val = all_elements_2d(list)
output = sum(each == 1 for each in val)
print(output)