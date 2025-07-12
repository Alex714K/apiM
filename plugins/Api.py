import datetime
import logging
import multiprocessing
from multiprocessing.sharedctypes import Synchronized

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
    CREDENTIALS_FILE_WB = "WildberriesPython.json"
    CREDENTIALS_FILE_OZON = "OzonPython.json"


    def __init__(self):
        self.logger = logging.getLogger()
        load_dotenv()
        activate_loggers()

        # self.lock: Synchronized = lock

        self.last_update_time = datetime.datetime.today()
        self.service_wb = self.create_service("WB")
        self.service_ozon = self.create_service("Ozon")

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        :return: None
        """
        match folder:
            case 'WB':
                ApiWB(self.get_service).start(name_of_sheet, who_is)
            case 'Ozon':
                ApiOzon(self.get_service).start(name_of_sheet, who_is)

    def get_service(self, folder: str):
        """
        Выполняет подключение к сервису Google.
        :return: Возвращает bool ответ результата подключения
        """
        # if (datetime.datetime.today() - self.last_update_time) < datetime.timedelta(seconds=5):
        #     time.sleep(5)
        service = None
        match folder:
            case "WB":
                service = self.service_wb
            case "Ozon":
                service = self.service_ozon

        return service

    def create_service(self, folder: str):
        CREDENTIALS_FILE = ""

        # while self.lock.value > 1:
        #     time.sleep(1)
        # if self.lock.value == 0:
        #     self.lock.value += 1
        #
        # time.sleep(10)

        match folder:
            case "WB":
                CREDENTIALS_FILE = self.CREDENTIALS_FILE_WB
            case "Ozon":
                CREDENTIALS_FILE = self.CREDENTIALS_FILE_OZON
        # Читаем ключи из файла
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE,
                                                                            scopes=scopes)
        try:
            service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
        except httplib2.error.ServerNotFoundError:
            self.logger.warning("Google: ServerNotFound")
            time.sleep(2)
            return self.get_service(folder)
        except socket.gaierror:
            self.logger.warning("gaierror with Google")
            time.sleep(2)
            return self.get_service(folder)

        # if self.lock.value > 0:
        #     self.lock.value -= 1

        return service
