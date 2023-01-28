from multiprocessing import Pool, cpu_count
from traceback import print_exc

import data
import notebook

running_tasks = {}
results = {}


def write_output():
    for n, output in list(results.items()):
        if data.insert_output(output):
            del results[n]


def process_result(output: dict):
    n = int(output.get('n'))
    results.update({n: output})
    del running_tasks[n]


def process_error(error: BaseException):
    print_exc()


cpus = cpu_count() - 1
with Pool(processes=cpus) as pool:
    while True:
        write_output()
        if len(running_tasks) < cpus:
            n = data.get_n()
            if n is None:
                continue
            try:
                running_tasks.update({
                    n: pool.apply_async(
                        notebook.run,
                        args=(n,),
                        callback=process_result,
                        error_callback=process_error
                    )
                })
            except:
                print_exc()
