from plugins.Wildberries.ApiWB import ApiWB
from plugins.Ozon.ApiOzon import ApiOzon
import threading


class Api:
    def __init__(self):
        self.lock_wb_request = threading.RLock()
        self.lock_ozon_request = threading.RLock()
        self.lock_wb_result = threading.RLock()
        self.lock_ozon_result = threading.RLock()

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        """
        match folder:
            case 'WB':
                wb_thread = threading.Thread(target=ApiWB(self.lock_wb_request, self.lock_wb_result).start,
                                             args=(name_of_sheet, who_is),
                                             name=f"WB, {name_of_sheet}, {who_is}")
                wb_thread.start()
            case 'Ozon':
                ozon_thread = threading.Thread(target=ApiOzon(self.lock_ozon_request, self.lock_ozon_result).start,
                                               args=(name_of_sheet, who_is),
                                               name=f"Ozon, {name_of_sheet}, {who_is}")
                ozon_thread.start()
