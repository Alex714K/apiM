import datetime
from plugins.Wildberries.ApiWB import ApiWB
from plugins.Ozon.ApiOzon import ApiOzon
from dotenv import load_dotenv
import threading
from plugins.Logger.Logger import activate_loggers


class Api:
    def __init__(self):
        self.lock_wb_request = threading.RLock()
        self.lock_ozon_request = threading.RLock()
        self.lock_wb_result = threading.RLock()
        self.lock_ozon_result = threading.RLock()
        load_dotenv()
        activate_loggers()

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        """
        match folder:
            case 'WB':
                name = f"WB, {name_of_sheet}, {who_is}, {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}"
                wb_thread = threading.Thread(target=ApiWB(self.lock_wb_request, self.lock_wb_result).start,
                                             args=(name_of_sheet, who_is),
                                             name=name)
                wb_thread.start()
            case 'Ozon':
                name = f"Ozon, {name_of_sheet}, {who_is}, {datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")}"
                ozon_thread = threading.Thread(target=ApiOzon(self.lock_ozon_request, self.lock_ozon_result).start,
                                               args=(name_of_sheet, who_is),
                                               name=name)
                ozon_thread.start()
