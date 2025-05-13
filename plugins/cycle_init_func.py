import time
from multiprocessing import Process
import schedule
from plugins.cycles.WB_cycle import wb_cycle
from plugins.cycles.Ozon_cycle import ozon_cycle


def launch():
    processes = [Process(target=wb_cycle), Process(target=ozon_cycle)]

    for process in processes:
        process.start()

    # for process in processes:
    #     process.join()

    while True:
        for i in range(len(processes)):
            if not processes[i].is_alive():
                processes[i].kill()
                if i == 0:
                    processes[i] = Process(target=wb_cycle)
                elif i == 1:
                    processes[i] = Process(target=ozon_cycle)
                processes[i].start()
        time.sleep(2)
