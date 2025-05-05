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
from plugins.logger.Logger import activate_loggers


class Api:
    def __init__(self):
        self.lock_wb_request = threading.RLock()
        self.lock_ozon_request = threading.RLock()
        self.lock_wb_result = threading.RLock()
        self.lock_ozon_result = threading.RLock()
        self.lock_wb_file_change_formats = threading.RLock()
        self.lock_ozon_file_change_formats = threading.RLock()
        self.lock_google = threading.Lock()
        self.logger = logging.getLogger()
        self.service = None
        load_dotenv()
        activate_loggers()
        self.connect_to_google()

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        :return: None
        """
        match folder:
            case 'WB':
                name = f"WB, {name_of_sheet}, {who_is}, {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}"
                locks = {
                    "LockWbRequest": self.lock_wb_request,
                    "LockWbResult": self.lock_wb_result,
                    "LockWbFile_ChangeFormats": self.lock_wb_file_change_formats,
                    "lock_Google": self.lock_google,
                }
                # wb_thread = threading.Thread(target=ApiWB(self.service, **locks).start,
                #                              args=(name_of_sheet, who_is, folder,),
                #                              name=name)
                # wb_thread.start()
                ApiWB(self.service, **locks).start(name_of_sheet, who_is)
            case 'Ozon':
                name = f"Ozon, {name_of_sheet}, {who_is}, {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}"
                locks = {
                    "LockOzonRequest": self.lock_ozon_request,
                    "LockOzonResult": self.lock_ozon_result,
                    "LockOzonFile_ChangeFormats": self.lock_ozon_file_change_formats,
                    "lock_Google": self.lock_google
                }
                # ozon_thread = threading.Thread(target=ApiOzon(self.service, **locks).start,
                #                                args=(name_of_sheet, who_is, folder,),
                #                                name=name)
                # ozon_thread.start()
                ApiOzon(self.service, **locks).start(name_of_sheet, who_is)

    def connect_to_google(self):
        """
        Выполняет подключение к сервису Google.
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
            self.logger.warning("Google: ServerNotFound")
            time.sleep(2)
            return self.connect_to_google()
        except socket.gaierror:
            self.logger.warning("gaierror with Google")
            time.sleep(2)
            return self.connect_to_google()
        finally:
            self.logger.debug("Connected to Google")
        self.service = service
