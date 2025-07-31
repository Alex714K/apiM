import datetime
import time
import socket
from argparse import ArgumentError
from logging import getLogger
from threading import Thread, Lock

import httplib2
import googleapiclient.errors
import googleapiclient.discovery
from googleapiclient.discovery_cache.base import Cache
from google.oauth2 import service_account
from dotenv import load_dotenv

from plugins.Wildberries.ApiWB import ApiWB
from plugins.Ozon.ApiOzon import ApiOzon
from plugins.logger.Logger import activate_loggers
from plugins.navigation.ClientEnum import Client
from plugins.navigation.FolderEnum import Folder
from plugins.navigation.NameOfSheetEnum import NameOfSheet


class Api:
    CREDENTIALS_FILE_WB = "WildberriesPython.json"
    CREDENTIALS_FILE_OZON = "OzonPython.json"


    def __init__(self):
        self.logger = getLogger()
        load_dotenv()
        activate_loggers()

        self.read_lock: Lock = Lock()
        self.write_lock: Lock = Lock()

    def create_thread(self, folder: Folder, who_is: Client, name_of_sheet: NameOfSheet) -> Thread:
        """
        Основной старт потока. От него зависит, что запуститься. Ничего не возвращает.
        :return: None
        """
        thread: Thread
        match folder:
            case Folder.WB:
                thread = Thread(target=ApiWB(self.create_service, self.read_lock, self.write_lock).execute, args=(who_is, name_of_sheet))
                # ApiWB(self.create_service).create_thread(who_is, name_of_sheet)
            case Folder.Ozon:
                thread = Thread(target=ApiOzon(self.create_service, self.read_lock, self.write_lock).execute, args=(who_is, name_of_sheet))
                # ApiOzon(self.create_service).create_thread(who_is, name_of_sheet)
            case _:
                raise ValueError("Wrong argument")

        thread.start()
        return thread

    def create_service(self, folder: Folder):
        CREDENTIALS_FILE = ""

        match folder:
            case Folder.WB:
                CREDENTIALS_FILE = self.CREDENTIALS_FILE_WB
            case Folder.Ozon:
                CREDENTIALS_FILE = self.CREDENTIALS_FILE_OZON
        # Читаем ключи из файла
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE,
                                                                            scopes=scopes)
        try:
            service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials, cache=MemoryCache())
        except httplib2.error.ServerNotFoundError:
            self.logger.warning("Google: ServerNotFound")
            time.sleep(2)
            return self.create_service(folder)
        except socket.gaierror:
            self.logger.warning("gaierror with Google")
            time.sleep(2)
            return self.create_service(folder)

        return service

class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content
