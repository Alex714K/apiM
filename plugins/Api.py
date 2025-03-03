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
        self.LockWbRequest = threading.RLock()
        self.LockOzonRequest = threading.RLock()
        self.LockWbResult = threading.RLock()
        self.LockOzonResult = threading.RLock()
        self.LockWbFile_ChangeFormats = threading.RLock()
        self.LockOzonFile_ChangeFormats = threading.RLock()
        self.lock_Google = threading.Lock()
        self.logger = logging.getLogger()
        self.service = None
        load_dotenv()
        activate_loggers()
        self.connect_to_Google()

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        :return: None
        """
        match folder:
            case 'WB':
                name = f"WB, {name_of_sheet}, {who_is}, {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}"
                locks = {
                    "LockWbRequest": self.LockWbRequest,
                    "LockWbResult": self.LockWbResult,
                    "LockWbFile_ChangeFormats": self.LockWbFile_ChangeFormats,
                    "lock_Google": self.lock_Google,
                }
                # wb_thread = threading.Thread(target=ApiWB(self.service, **locks).start,
                #                              args=(name_of_sheet, who_is, folder,),
                #                              name=name)
                # wb_thread.start()
                ApiWB(self.service, **locks).start(name_of_sheet, who_is)
            case 'Ozon':
                name = f"Ozon, {name_of_sheet}, {who_is}, {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}"
                locks = {
                    "LockOzonRequest": self.LockOzonRequest,
                    "LockOzonResult": self.LockOzonResult,
                    "LockOzonFile_ChangeFormats": self.LockOzonFile_ChangeFormats,
                    "lock_Google": self.lock_Google
                }
                # ozon_thread = threading.Thread(target=ApiOzon(self.service, **locks).start,
                #                                args=(name_of_sheet, who_is, folder,),
                #                                name=name)
                # ozon_thread.start()
                ApiOzon(self.service, **locks).start(name_of_sheet, who_is)

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
