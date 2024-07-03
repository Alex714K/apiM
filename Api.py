from Initers import Initer
import logging
from Wildberries.ApiWB import ApiWB
from Ozon.ApiOzon import ApiOzon
from datetime import datetime
import threading


class Api(Initer):
    @staticmethod
    def start(name_of_sheet: str, who_is: str, folder: str, dateFrom: str = None, date: str = None,
              flag: str = None, filterNmID=None, limit: str = None, dateTo: str = None, from_rk: str = None,
              to_rk: str = None):
        """Основной старт. От него зависит, что запуститься. Ничего не возвращает."""
        print('-------------------------------------------------------------------------------------------------------')
        print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {folder}, {who_is}, {name_of_sheet}")
        logging.info(f"Started '{name_of_sheet}'")
        match folder:
            case 'WB':
                wb_thread = threading.Thread(target=ApiWB().start,
                                             args=(name_of_sheet, who_is, dateFrom, dateTo, date, flag, filterNmID,
                                                   limit, from_rk, to_rk))
                wb_thread.start()
            case 'Ozon':
                ozon_thread = threading.Thread(target=ApiOzon().start,
                                               args=(name_of_sheet, who_is))
                ozon_thread.start()
