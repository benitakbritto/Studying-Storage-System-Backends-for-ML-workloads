# will form only if we fix ds, input size
import argparse
import csv 
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument(
    "-input-file", 
    type=str, 
    help="Name of the input file(s). Accepts wildcards.",
    nargs='+'
)
parser.add_argument(
    "-output-file", 
    type=str, 
    help="Name of the output file",
)
args = parser.parse_args()

# data_store = ''
input_size = 1
worker = 0
rows_per_key = 1
type = ''
batch_size = 1
prefetch_size = 1
output_file = ''

def read_file_name(file_name):
    global input_size
    global worker
    global rows_per_key
    global type 
    global batch
    global prefetch_size

    file_name = file_name.split('/')[-1]
    file_name_list = file_name.split('_')

    for val in file_name_list:
        if val[0] == 'i':
            input_size = int(val[1:])
        elif val[0] == 'w':
            worker = int(val[1:])
        elif val[0] == 'r':
            rows_per_key = int(val[1:])
        elif val[0] == 't':
            type = val[1:]
        elif val[0] == 'b':
            batch_size = int(val[1:])
        elif val[0] == 'p':
            prefetch_size = int(val[1:])
    
    print(f'input_size = {input_size}, worker = {worker}, rows_per_key = {rows_per_key}, type = {type}, batch_size = {batch_size}, prefetch_size = {prefetch_size}')

def get_file_content(file_name):
    write_time = 0
    read_time = 0

    with open(file_name) as f:
        for index, line in enumerate(f):
                if index == 2:
                    line = line.split()
                    write_time = float(line[3])
                elif index == 3:
                    line = line.split()
                    read_time = float(line[4])

    
    return write_time, read_time

def run_parser():
    measurements = defaultdict(list)

    # collect metrics
    for input_file in args.input_file:
        print(f'[DEBUG] input_file = {input_file}')
        read_file_name(input_file)
        write, read = get_file_content(input_file)
        print(f'[DEBUG] write = {write}, read = {read}')

        key = ''
        if type == 'm':
            key = f'w{worker}_r{rows_per_key}_t{type}_b{batch_size}'
        else:
            key = f'w{worker}_r{rows_per_key}_t{type}_b{batch_size}_p{prefetch_size}'
        
        print(f'[DEBUG] key = {key}')
        measurements[key].append(write)
        measurements[key].append(read)

    # convert to csv
    # TODO

if __name__ == "__main__":
    run_parser()

