from Initers import Initer
import logging
from Wildberries.ApiWB import ApiNew
from datetime import datetime


class Api(Initer):
    @staticmethod
    def start(name_of_sheet: str, who_is: str, folder: str, dateFrom: str = None, date: str = None,
              flag: str = None, filterNmID=None, limit: str = None, dateTo: str = None, from_rk: str = None,
              to_rk: str = None):
        """Основной старт. От него зависит, что запуститься. Ничего не возвращает."""
        print('-------------------------------------------------------------------------------------------------------')
        print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {name_of_sheet}, {who_is}")
        logging.info(f"Started '{name_of_sheet}'")
        match folder:
            case 'WB':
                ApiNew().start(name_of_sheet, who_is, dateFrom=dateFrom, dateTo=dateTo, date=date, flag=flag,
                               filterNmID=filterNmID, limit=limit, from_rk=from_rk, to_rk=to_rk)
