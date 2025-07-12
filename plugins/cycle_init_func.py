import ctypes
import time
from multiprocessing import Process, Value
from typing import Any

from plugins.Api import Api
from plugins.cycles.WB_cycle import wb_cycle
from plugins.cycles.Ozon_cycle import ozon_cycle
from plugins.update_data import UpdateAndSchedules
from plugins.Wildberries.create_process_for_client import create_process_for_client as create_process_wb
from plugins.Ozon.create_process_for_client import create_process_for_client as create_process_ozon


def launch() -> Any:
    processes_wb: list[Process] = list()
    processes_ozon: list[Process] = list()
    lock = Value('i', 0)

    for client, update_time in UpdateAndSchedules.clients_wb:
        processes_wb.append(create_process_wb(lock, client, "WB", update_time))
        print(f"Configured {client} from Wildberries")
        time.sleep(1)

    for client, update_time in UpdateAndSchedules.clients_ozon:
        processes_ozon.append(create_process_ozon(lock, client, "Ozon", update_time))
        print(f"Configured {client} from Ozon")
        time.sleep(1)

    for process in processes_wb:
        process.start()
    for process in processes_ozon:
        process.start()

    time.sleep(5)

    print("\nStarted processes successfully")
    print("Starting checking processes in main process\n")

    while True:
        for i in range(len(processes_wb)):
            if not processes_wb[i].is_alive():
                processes_wb[i].kill()
                processes_wb[i] = create_process_wb(UpdateAndSchedules.clients_wb[i][0], "WB",
                                                    UpdateAndSchedules.clients_wb[i][1])
                processes_wb[i].start()

        for i in range(len(processes_ozon)):
            if not processes_ozon[i].is_alive():
                processes_ozon[i].kill()
                processes_ozon[i] = create_process_ozon(UpdateAndSchedules.clients_ozon[i][0], "Ozon",
                                                        UpdateAndSchedules.clients_ozon[i][1])
                processes_ozon[i].start()

        time.sleep(5)
        print(lock.value)


def launch_beta():
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
