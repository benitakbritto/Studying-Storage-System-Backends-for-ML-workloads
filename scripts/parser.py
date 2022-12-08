'''
    @brief: Transform all the output files -> csv
    @prereq: bash
    @command: python parser.py -input-file ../output/*
    @authors: Benita, Hemal, Reetuparna
'''

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
args = parser.parse_args()

# Globals
input_size = 1
worker = 0
rows_per_key = 1
type = ''
batch_size = 1
prefetch_size = 1
data_store = ''
workload = ''
data_store_list = ['rd', 'td', 'ts']
type_list = ['m', 'i']
batch_size_list = [128, 256, 512, 1024]
prefetch_size_list = [128, 256, 512, 1024]
rows_per_key_list = [1, 128, 256, 512, 1024]
workers_list = [0, 8, 16, 32]
workload_list = ['text', 'image', 'graph']

# For debug
count_rd_map = 0
count_rd_iter = 0
count_td_map = 0
count_td_iter = 0
count_ts_map = 0
count_ts_iter = 0

def debug(ds, dataloader_type):
    global count_rd_map
    global count_rd_iter
    global count_td_map
    global count_td_iter
    global count_ts_map
    global count_ts_itr

    print(f'[DEBUG] ds = {ds}, dataloader_type = {dataloader_type}')

    if ds == 'rd':
        if dataloader_type == 'm':
            count_rd_map += 1
        elif dataloader_type == 'i':
            count_rd_iter += 1
    elif ds == 'td':
        if dataloader_type == 'm':
            count_td_map += 1
        elif dataloader_type == 'i':
            count_td_iter += 1
    elif ds == 'ts':
        if dataloader_type == 'm':
            count_ts_map += 1
        elif dataloader_type == 'i':
            count_ts_itr += 1

def read_file_name(file_name):
    # print(f'[DEBUG] file_name = {file_name}')
    global input_size
    global worker
    global rows_per_key
    global type 
    global batch
    global prefetch_size
    global data_store
    global workload

    file_name = file_name.split('/')
    workload = file_name[-2]
    data_store = file_name[-3]
    file_name_list = file_name[-1].split('_')

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
    
    # print(f'[DEBUG] input_size = {input_size}, \
    #     worker = {worker}, \
    #     rows_per_key = {rows_per_key}, \
    #     type = {type}, \
    #     batch_size = {batch_size}, \
    #     prefetch_size = {prefetch_size}, \
    #     data_store = {data_store}, \
    #     workload = {workload}')

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
    collect_metrics(measurements)
    # TODO: Uncomment later
    # write_to_csv(measurements)

    print(f'[DEBUG] count_rd_map = {count_rd_map} \
        count_rd_iter = {count_rd_iter} \
        count_td_map = {count_td_map} \
        count_td_iter = {count_td_iter} \
        count_ts_map = {count_ts_map} \
        count_ts_iter = {count_ts_iter}')

def collect_metrics(measurements):
    for input_file in args.input_file:
        # print(f'[DEBUG] input_file = {input_file}')
        # TODO: Uncomment later
        read_file_name(input_file)
        debug(data_store, type)
        # write, read = get_file_content(input_file)
        # print(f'[DEBUG] write = {write}, read = {read}')

        key = ''
        if type == 'm':
            key = f'{data_store}_{workload}_w{worker}_r{rows_per_key}_t{type}_b{batch_size}'
        else:
            key = f'{data_store}_{workload}_w{worker}_r{rows_per_key}_t{type}_b{batch_size}_p{prefetch_size}'
        
        # print(f'[DEBUG] key = {key}')
        # TODO: Uncomment later
        # measurements[key].append(write)
        # measurements[key].append(read)
        measurements[key].append(0)
        measurements[key].append(0)

def write_to_csv(measurements):
    for item in workload_list:
        for t in type_list:
            if t == 'm':
                for r in rows_per_key_list:
                    csv_file_data = []
                    for b in batch_size_list:
                        row_data = []
                        for w in workers_list:
                            for ds in data_store_list:
                                key = f'{ds}_{item}_w{w}_r{r}_t{t}_b{b}'
                                # print(f'[DEBUG] try for key = {key}')
                                if key in measurements and len(measurements[key]) == 2:
                                    row_data.append(measurements[key][0]) # write
                                    row_data.append(measurements[key][1]) # read
                                else:
                                    print(f'[INFO] {key} does not exist or len is not 2')
                                    row_data.append(None)
                                    row_data.append(None)
                                
                        csv_file_data.append(row_data)
                    
                    output_file_name = f'{item}_r{r}_t{t}.csv'
                    # TODO: Uncomment later
                    # with open(output_file_name, 'w', encoding='UTF8') as f:
                    #     writer = csv.writer(f)
                    #     for row in csv_file_data:
                    #         writer.writerow(row)

            elif t == 'i':
                for p in prefetch_size_list:
                    csv_file_data = []
                    for b in batch_size_list:
                        row_data = []
                        for w in workers_list:
                            for ds in data_store_list:
                                key = f'{ds}_{item}_w{w}_r1_t{t}_b{b}_p{p}'
                                # print(f'[DEBUG] try for key = {key}')
                                if key in measurements and len(measurements[key]) == 2:
                                    row_data.append(measurements[key][0]) # write
                                    row_data.append(measurements[key][1]) # read
                                else:
                                    print(f'[INFO] {key} does not exist or len is not 2')
                                    row_data.append(None)
                                    row_data.append(None)
                        csv_file_data.append(row_data)
                    
                    output_file_name = f'{item}_p{p}_t{t}.csv'
                    # TODO: Uncomment later
                    # with open(output_file_name, 'w', encoding='UTF8') as f:
                    #     writer = csv.writer(f)
                    #     for row in csv_file_data:
                    #         writer.writerow(row)

if __name__ == "__main__":
    run_parser()
