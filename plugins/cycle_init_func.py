import time
from multiprocessing import Process
import schedule
from plugins.cycles.WB_cycle import WB_cycle
from plugins.cycles.Ozon_cycle import Ozon_cycle


def launch():
    processes = [Process(target=WB_cycle), Process(target=Ozon_cycle)]

    for process in processes:
        process.start()

    while True:
        for process in processes:
            if not process.is_alive():
                process.kill()
                process.run()
        time.sleep(1)
