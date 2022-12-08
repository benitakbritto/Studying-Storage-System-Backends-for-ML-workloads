import numpy as np
import argparse
import random

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-size",
    help="Dataset size",
    default=1000,
    required=True)

parser.add_argument("-output-file",
    help="Path to the output file",
    required=True)

parser.add_argument("-type", 
    help = "type of distribution to generate", 
    choices=['zipf', 'power'],
    required=True)

# Read arguments from command line
args = parser.parse_args()

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

size = int(args.size)

data = None

if args.type == 'zipf':
    data = gen_zipf(size)
elif args.type == 'power':
    data = gen_powerlaw(size)
else:
    NotImplementedError("not supported yet")

np.savetxt(args.output_file, data, fmt='%d')