from os.path import exists

# Globals
file_prefix = '../output'
input_size = 1
data_store_list = ['rd', 'td', 'ts']
type_list = ['m', 'i']
batch_size_list = [128, 256, 512, 1024]
prefetch_size_list = [128, 256, 512, 1024]
rows_per_key_list = [1, 128, 256, 512, 1024]
workers_list = [0, 8, 16, 32]
workload_list = ['text', 'image', 'graph']

count_rd_text_map = 0
count_rd_text_iter = 0
count_rd_image_map = 0
count_rd_image_iter = 0
count_rd_graph_map = 0
count_rd_graph_iter = 0

count_td_text_map = 0
count_td_text_iter = 0
count_td_image_map = 0
count_td_image_iter = 0
count_td_graph_map = 0
count_td_graph_iter = 0

count_ts_text_map = 0
count_ts_text_iter = 0
count_ts_image_map = 0
count_ts_image_iter = 0
count_ts_graph_map = 0
count_ts_graph_iter = 0

def check_file(file_name):
    if exists(file_name):
        with open(file_name, 'r') as f:
            for index, line in enumerate(f):
                line = line.split()
                # file is correct
                if len(line) == 6 and line[1] == 'Dataloader':
                    return True
                    break
    
        print(f'[INFO] {file_name} exists, but does not contain right data')
        return False

    else:
        print(f'[INFO] {file_name} does not exist')
        return False

def update_count(check_file_val, data_store, workload, type):
    global count_rd_text_map
    global count_rd_text_iter
    global count_rd_image_map
    global count_rd_image_iter
    global count_rd_graph_map
    global count_rd_graph_iter

    global count_td_text_map
    global count_td_text_iter
    global count_td_image_map
    global count_td_image_iter
    global count_td_graph_map
    global count_td_graph_iter

    global count_ts_text_map
    global count_ts_text_iter
    global count_ts_image_map
    global count_ts_image_iter
    global count_ts_graph_map
    global count_ts_graph_iter

    if check_file_val == True:
        if data_store == 'rd' and workload == 'text' and type == 'm':
            count_rd_text_map += 1
        elif data_store == 'rd' and workload == 'text' and type == 'i':
            count_rd_text_iter += 1
        elif data_store == 'rd' and workload == 'image' and type == 'm':
            count_rd_image_map += 1
        elif data_store == 'rd' and workload == 'image' and type == 'i':
            count_rd_image_iter += 1
        elif data_store == 'rd' and workload == 'graph' and type == 'm':
            count_rd_graph_map += 1
        elif data_store == 'rd' and workload == 'graph' and type == 'i':
            count_rd_graph_iter += 1
        
        elif data_store == 'td' and workload == 'text' and type == 'm':
            count_td_text_map += 1
        elif data_store == 'td' and workload == 'text' and type == 'i':
            count_td_text_iter += 1
        elif data_store == 'td' and workload == 'image' and type == 'm':
            count_td_image_map += 1
        elif data_store == 'td' and workload == 'image' and type == 'i':
            count_td_image_iter += 1
        elif data_store == 'td' and workload == 'graph' and type == 'm':
            count_td_graph_map += 1
        elif data_store == 'td' and workload == 'graph' and type == 'i':
            count_td_graph_iter += 1

        if data_store == 'ts' and workload == 'text' and type == 'm':
            count_ts_text_map += 1
        elif data_store == 'ts' and workload == 'text' and type == 'i':
            count_ts_text_iter += 1
        elif data_store == 'ts' and workload == 'image' and type == 'm':
            count_ts_image_map += 1
        elif data_store == 'ts' and workload == 'image' and type == 'i':
            count_ts_image_iter += 1
        elif data_store == 'ts' and workload == 'graph' and type == 'm':
            count_ts_graph_map += 1
        elif data_store == 'ts' and workload == 'graph' and type == 'i':
            count_ts_graph_iter += 1

def run_checker():    
    for data_store in data_store_list:
        for workload in workload_list: 
            for workers in workers_list:
                for type in type_list:
                    if type ==  'm':
                        for batch_size in batch_size_list:
                            if data_store == 'rd':
                                for rows_per_key in rows_per_key_list:
                                    file_name = f'{file_prefix}/{data_store}/{workload}/i{1}_w{workers}_r{rows_per_key}_t{type}_b{batch_size}'
                                    ret = check_file(file_name)
                                    update_count(ret, data_store, workload, type)
                            else:
                                file_name = f'{file_prefix}/{data_store}/{workload}/i{1}_w{workers}_r1_t{type}_b{batch_size}'
                                ret = check_file(file_name)
                                update_count(ret, data_store, workload, type)
                    
                    elif type == 'i':
                        for batch_size in batch_size_list:
                            for prefetch_size in prefetch_size_list:
                                file_name = f'{file_prefix}/{data_store}/{workload}/i{1}_w{workers}_r1_t{type}_b{batch_size}_p{prefetch_size}'
                                ret = check_file(file_name)
                                update_count(ret, data_store, workload, type)
       
if __name__ == "__main__":
    run_checker()

    print(f'[INFO] count_rd_text_map = {count_rd_text_map} / 80 \n \
        count_rd_text_iter = {count_rd_text_iter} / 64 \n \
        count_rd_image_map = {count_rd_image_map} / 80 \n \
        count_rd_image_iter = {count_rd_image_iter} / 64 \n \
        count_rd_graph_map = {count_rd_graph_map} / 80 \n \
        count_rd_graph_iter = {count_rd_graph_iter} / 64 \n \
        count_td_text_map = {count_td_text_map} / 16 \n \
        count_td_text_iter = {count_td_text_iter} / 64 \n \
        count_td_image_map = {count_td_image_map} / 16 \n \
        count_td_image_iter = {count_td_image_iter} / 64 \n \
        count_td_graph_map = {count_td_graph_map} / 16 \n \
        count_td_graph_iter = {count_td_graph_iter} / 64 \n \
        count_ts_text_map = {count_ts_text_map} / 16 \n \
        count_ts_text_iter = {count_ts_text_iter} / 0 \n \
        count_ts_image_map = {count_ts_image_map} / 16 \n \
        count_ts_image_iter = {count_ts_image_iter} / 64 \n \
        count_ts_graph_map = {count_ts_graph_map} / 16 \n \
        count_ts_graph_iter = {count_ts_graph_iter} / 0 \n')
