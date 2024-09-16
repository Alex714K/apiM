import datetime
import http.client
import socket
import ssl
import threading
import time
import googleapiclient.errors
from googleapiclient.discovery import build
import csv
from plugins.Ozon.Converter_to_list_Ozon import Converter
from plugins.Ozon.Request_Ozon import RequestOzon
from logging import getLogger
from plugins.google_main_functions import GoogleMainFunctions
import os


class ApiOzon(Converter, GoogleMainFunctions):
    def __init__(self, service: googleapiclient.discovery.build, **kwargs: threading.RLock):
        super().__init__(**kwargs)
        self.service = service
        self.values, self.dist, self.needed_keys = None, None, None
        self.result = None
        self.name_of_sheet = None
        self.who_is = None
        self.folder = None
        self.LockOzonRequest = kwargs["LockOzonRequest"]
        self.LockOzonResult = kwargs["LockOzonResult"]
        self.LockOzonFile_ChangeFormats = kwargs["LockOzonFile_ChangeFormats"]
        self.logger = getLogger("ApiOzon")

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Запуск работы с запросом на сервера Ozon.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :param folder: В какую папку идти
        :return:
        """
        self.logger.info(f"Started: folder=Ozon, who_is={who_is}, name_of_sheet={name_of_sheet}")
        if name_of_sheet == "update_Results":
            self.update_Results(who_is)
        self.folder = folder
        if not self.standart_start(name_of_sheet, who_is):
            return
        match name_of_sheet:
            case 'analytics':
                self.analytics_update(who_is)
            case _:
                self.standart_update(name_of_sheet, who_is)

    def standart_start(self, name_of_sheet: str, who_is: str):
        self.name_of_sheet = name_of_sheet
        self.who_is = who_is
        if not self.start_work_with_request(name_of_sheet, who_is):
            return False
        return True

    def standart_update(self, name_of_sheet: str, who_is: str):
        self.choose_spreadsheetId(who_is)
        new_or_not = self.choose_name_of_sheet(name_of_sheet, who_is)
        if new_or_not == 'error':
            return
        if new_or_not:
            check = self.create_sheet(name_of_sheet=name_of_sheet)
        else:
            check = self.update_sheet(name_of_sheet=name_of_sheet)
        if check:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        elif self.result is not None:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
        else:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)

    def analytics_update(self, who_is: str):
        self.choose_spreadsheetId(f"{self.who_is}-analytics")
        today = datetime.date.today()
        if today.day == 1:
            name_of_sheet = datetime.date(today.year, today.month - 1, 31).strftime("%b")
        else:
            name_of_sheet = today.strftime("%b")
        self.choose_name_of_sheet(name_of_sheet, f"{self.who_is}-analytics")

        # new_or_not = self.choose_name_of_sheet(name_of_sheet=name_of_sheet)
        # if new_or_not == 'error':
        #     return
        # if new_or_not:
        #     check = self.create_sheet(name_of_sheet=name_of_sheet)
        # else:
        check = self.update_sheet(name_of_sheet=name_of_sheet)
        if check:
            self.start_work_with_list_result(name_of_sheet="analytics")
        elif self.result is not None:
            self.start_work_with_list_result(name_of_sheet="analytics", bad=True)
        else:
            self.start_work_with_list_result(name_of_sheet="analytics", bad=True)

    def choose_spreadsheetId(self, who_is: str):
        """
        Записывает в self.spreadsheetId Id Таблицы, с которой надо будет работать.
        :param who_is:
        :return:
        """
        self.spreadsheetId = os.getenv(f"Ozon-spreadsheetid-{who_is}")

    def start_work_with_request(self, name_of_sheet: str, who_is: str):
        requestOzon = RequestOzon(self.LockOzonRequest).start(name_of_sheet, who_is)
        match requestOzon:
            case 'Missing json file':
                self.logger.warning("Не получен файл с Ozon - start_work_with_request")
                self.result = 'ERROR: Не получен файл с Ozon'
                return False
            case 'Проблема с соединением':
                self.logger.warning("Проблема с соединением - RequestOzon - start_work_with_request")
                self.result = 'ERROR: Проблема с соединением'
                return False
        if type(requestOzon) == tuple:
            if type(requestOzon[0]) == int and requestOzon[0] != 200:
                self.result = f'ERROR: {requestOzon[1]}'
                return False
        try:
            json_response = requestOzon
        except TypeError:
            self.logger.warning(f"Нет доступа к файлу - start_work_with_request")
            # print(f"Нет доступа к файлу ({self.name_of_sheet})")
            return False
        result = self.convert_to_list(json_response, name_of_sheet)
        match result:
            case 'download':
                self.logger.info(f"Downloaded {name_of_sheet} - start_work_with_request")
                self.result = 'Зачем-то скачен файл'
                return False
            case 'is None':
                self.logger.warning(f"File({self.name_of_sheet}) = None - start_work_with_request")
                self.result = 'ERROR: File=None'
                return False
            case 'is empty':
                self.logger.warning(f"File({self.name_of_sheet}) is empty - start_work_with_request")
                self.result = 'ERROR: File is empty'
                return False
        self.values, self.dist, self.needed_keys = result
        self.values = self.replace_from_dot_to_comma(self.values)
        return True

    def start_work_with_list_result(self, name_of_sheet: str, bad: bool = False):
        """
        Пишет результат работы с листом в таблицу 'Result'. При отстутсвии таковой создаёт её и только после этого
        добавляет туда результат.

        В результате пишутся дата обновления и результат (количество успешно записанных строк или ошибку)
        :param name_of_sheet: Название листа, в котором пытались сделать обновление
        :param bad: Успешно или нет
        :return:
        """
        self.LockOzonResult.acquire()
        design = list()
        with open('plugins/Ozon/data/info_about_Result_Ozon.csv', 'r', encoding='UTF-8') as file:
            csv_file = csv.reader(file)
            for row in csv_file:
                if '' == row:
                    continue
                else:
                    design.append(row)
        self.create_result(design)
        self.insert_new_info(design)
        self.LockOzonResult.release()
