'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename> --iterations <num> --input-file <path> --output-file <path>
    @authors: Benita, Hemal, Reetuparna
'''

from os import system
import argparse

parser = argparse.ArgumentParser(description='Concatenate a dataset to make it larger')
parser.add_argument('--iterations', type=int, default=2, help='The number of times the file will be concatenated')
parser.add_argument('--input-file', type=str, help='The path of the dataset to be concatenated')
parser.add_argument('--output-file', type=str, help='The path of the concatenated file')
args = parser.parse_args()

if __name__ == "__main__":
    print(f'[DEBUG] Iterations = {args.iterations}')
    print(f'[DEBUG] Input file = {args.input_file}')
    print(f'[DEBUG] Output file = {args.output_file}')

    for i in range(0, args.iterations):
        command_str = f'cat {args.input_file} >> {args.output_file}'
        system(command_str)
