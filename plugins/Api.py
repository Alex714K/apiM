import datetime
import logging
import httplib2
import googleapiclient.errors
import googleapiclient.discovery
import time
import socket
from google.oauth2 import service_account
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
        self.lock_Google = threading.Lock()
        self.logger = logging.getLogger()
        self.service = None
        load_dotenv()
        activate_loggers()
        self.connect_to_Google()

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        """
        match folder:
            case 'WB':
                name = f"WB, {name_of_sheet}, {who_is}, {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}"
                locks = {
                    "lock_wb_request": self.lock_wb_request,
                    "lock_wb_result": self.lock_wb_result,
                    "lock_Google": self.lock_Google
                }
                wb_thread = threading.Thread(target=ApiWB(self.service, **locks).start,
                                             args=(name_of_sheet, who_is),
                                             name=name)
                wb_thread.start()
            case 'Ozon':
                name = f"Ozon, {name_of_sheet}, {who_is}, {datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")}"
                locks = {
                    "lock_ozon_request": self.lock_ozon_request,
                    "lock_ozon_result": self.lock_ozon_result,
                    "lock_Google": self.lock_Google
                }
                ozon_thread = threading.Thread(target=ApiOzon(self.service, **locks).start,
                                               args=(name_of_sheet, who_is),
                                               name=name)
                ozon_thread.start()

    def connect_to_Google(self) -> bool:
        """
        Выполняет подключение к сервису Google
        :return: Возвращает bool ответ результата подключения
        """
        CREDENTIALS_FILE = 'Alex714K.json'
        # Читаем ключи из файла
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE,
                                                                            scopes=scopes)
        try:
            service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
        except httplib2.error.ServerNotFoundError:
            self.logger.warning(f"Google: ServerNotFound")
            time.sleep(2)
            return self.connect_to_Google()
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google")
            time.sleep(2)
            return self.connect_to_Google()
        finally:
            self.logger.debug(f"Connected to Google")
        self.service = service
        return True
