from multiprocessing import Pool, cpu_count

import data
import notebook

running_tasks = {}


def write_output(output: dict):
    data.insert_output(output)
    del running_tasks[output.get('n')]


cpus = cpu_count()
with Pool(processes=cpus) as pool:
    while True:
        if len(running_tasks) < cpus:
            n = data.get_n()
            running_tasks.update({n: pool.apply_async(notebook.run, args=(n,), callback=write_output)})
