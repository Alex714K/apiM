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
        for process in processes:
            if not process.is_alive():
                process.kill()
                process.run()
        time.sleep(2)
