from Initers import Initer
import logging
from Wildberries.ApiWB import ApiWB
from Ozon.ApiOzon import ApiOzon
from datetime import datetime
import threading


class Api(Initer):
    @staticmethod
    def start(name_of_sheet: str, who_is: str, folder: str):
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        """
        print(f"Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {folder}, {who_is}, {name_of_sheet}")
        logging.info(f"Started '{name_of_sheet}'")
        match folder:
            case 'WB':
                wb_thread = threading.Thread(target=ApiWB().start,
                                             args=(name_of_sheet, who_is),
                                             name=f"WB, {name_of_sheet}, {who_is}")
                wb_thread.start()
            case 'Ozon':
                ozon_thread = threading.Thread(target=ApiOzon().start,
                                               args=(name_of_sheet, who_is),
                                               name=f"Ozon, {name_of_sheet}, {who_is}")
                ozon_thread.start()
