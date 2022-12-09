import numpy as np
import random

def gen_zipf(size):
    a = 2.0

    # get zipf dist
    data = np.random.zipf(a, size)
    # print(data)

    # tranform into contiguous numbers
    data = np.unique(data, return_inverse=True)[1]

    return data

def gen_powerlaw(size):
    x_min = 5
    alpha = 2.5

    data = []

    for _ in range(0, size):
        x_smp = x_min * (1 - random.random()) ** (-1 / (alpha - 1))
        data.append(round(x_smp))

    data = np.array(data)

    # tranform into contiguous numbers
    data = np.unique(data, return_inverse=True)[1]

    return data

def gen(type, size, output_file):
    data = None

    if type == 'zipf':
        data = gen_zipf(size)
    elif type == 'power':
        data = gen_powerlaw(size)
    else:
        NotImplementedError("not supported yet")
    
    np.savetxt(output_file, data, fmt='%d')

    return data.max()