import time
from datetime import datetime, timedelta
from multiprocessing import Process
from multiprocessing.sharedctypes import Synchronized

import schedule

from plugins.Api import Api
from plugins.update_data import UpdateAndSchedules


def create_process_for_client(lock: Synchronized, client: str, folder: str, start_time: datetime) -> Process:
    return Process(target=schedule_all, args=(lock, client, folder, start_time))


def schedule_all(lock: Synchronized, client: str, folder: str, start_time: datetime):
    my_scheduler = schedule.Scheduler()
    for name_of_sheet in UpdateAndSchedules.names_of_sheet_wb_oneday:
        my_scheduler.every().day.at(start_time.strftime("%H:%M")).do(Api().create_thread, folder, client, name_of_sheet)
        start_time = start_time + timedelta(minutes=5)

    for name_of_sheet, interval in UpdateAndSchedules.names_of_sheet_wb_interval:
        my_scheduler.every(int(interval)).seconds.do(Api().create_thread, folder, client, name_of_sheet)

    while True:
        my_scheduler.run_pending()
        time.sleep(5)
