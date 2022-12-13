'''
    @brief: Transform all the output/monitor files -> csv
    @prereq: bash
    @command: python parse_monitor.py -input-file ../../output/monitor/*/*/1.txt
    @authors: Benita, Hemal, Reetuparna
'''

import argparse
import csv 
from collections import defaultdict
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument(
    "-input-file", 
    type=str, 
    help="Name of the input file(s). Accepts wildcards.",
    nargs='+'
)
args = parser.parse_args()

# Globals
# virtual_memory_key_list = ['total', 'available', 'percent', 'used', 'free', 'active', 'inactive', 'buffers', 'cached', 'shared', 'slab']
# swap_memory_key_list = ['total', 'used', 'free', 'percent', 'sin', 'sout']
# disk_usage_key_list = ['total', 'used', 'free', 'percent']
monitor_list = ['cpu', 'vm', 'sm', 'disk']
workload_list = ['text', 'image', 'graph']
data_store_list = ['base', 'rd', 'td', 'ts']

# returns aggrega
def process_cpu_percent(data):
    return np.sum([float(val) for val in data[1:-1].split(',')])

def process_virtual_memory(data):
    virtual_memory_list = []
    data = data.strip()[6:-1].split(',')
    for val in data:
        virtual_memory_list.append(val.split('=')[1])
    
    return virtual_memory_list[5]

def process_swap_memory(data):
    swap_memory_list = []
    data = data.strip()[11:-1].split(',')
    for val in data:
        swap_memory_list.append(val.split('=')[1])
    
    return swap_memory_list[1]

def process_disk_usage(data):
    disk_usage_list = []
    data = data.strip()[6:-1].split(',')
    for val in data:
        disk_usage_list.append(val.split('=')[1])
    
    return disk_usage_list[1]

def read_file_content(file_name):
    cpu_percent_list = []
    virtual_memory_list = []
    swap_memory_list = []
    disk_usage_list = []

    with open(file_name, 'r') as f:
        for line in f:
            line = line.split(':')
            if line[0] == 'cpu_percent':
                cpu_percent_list.append(process_cpu_percent(line[1].strip()))
            
            elif line[0] == 'virtual_memory':
                virtual_memory_list.append(process_virtual_memory(line[1].strip()))
            
            elif line[0] == 'swap_memory':
                swap_memory_list.append(process_swap_memory(line[1].strip()))

            elif line[0] == 'disk_usage':
                disk_usage_list.append(process_disk_usage(line[1].strip()))

    return cpu_percent_list, virtual_memory_list, swap_memory_list, disk_usage_list

def get_workload(file_path):
    return file_path.split('/')[-3]

def get_datastore(file_path):
    return file_path.split('/')[-2]

def run():
    file_data_dict = defaultdict(list)

    for input_file in args.input_file:
        workload = get_workload(input_file)
        datastore = get_datastore(input_file)
        cpu, vm, sm, disk = read_file_content(input_file)

        file_data_dict[f'{workload}_{datastore}_cpu'] = cpu
        file_data_dict[f'{workload}_{datastore}_vm'] = vm
        file_data_dict[f'{workload}_{datastore}_sm'] = sm
        file_data_dict[f'{workload}_{datastore}_disk'] = disk

    # import pdb; pdb.set_trace()
    
    for workload in workload_list:
        for monitor in monitor_list:
            output_file_name = f'{workload}_{monitor}.csv'
            with open(output_file_name, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data_store_list)
                min_len = np.min([len(file_data_dict[f'{workload}_{datastore}_{monitor}']) for datastore in data_store_list])
                for idx in range(min_len):
                    writer.writerow([file_data_dict[f'{workload}_{datastore}_{monitor}'][idx] for datastore in data_store_list])

if __name__ == "__main__":
    run()