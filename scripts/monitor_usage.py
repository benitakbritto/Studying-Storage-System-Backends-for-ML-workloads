'''
    @brief: Monitors cpu and mem usage
    @prereq: bash
    @command: python output_file_checker.py
    @authors: Benita, Hemal, Reetuparna
'''

import psutil

def run_monitor():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        disk_usage = psutil.disk_usage('/')

        print(f'cpu_percent: {cpu_percent}')
        print(f'virtual_memory: {virtual_memory}')
        print(f'swap_memory: {swap_memory}')
        print(f'disk_usage: {disk_usage}')
    
if __name__ == "__main__":
    run_monitor()