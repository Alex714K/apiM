import datetime
import calendar
import threading
import time
import googleapiclient.errors
import pandas
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

    def start(self, name_of_sheet: str, who_is: str):
        """
        Запуск работы с запросом на сервера Ozon.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return:
        """
        self.logger.info(f"Started: folder=Ozon, who_is={who_is}, name_of_sheet={name_of_sheet}")
        if name_of_sheet == "update_Results":
            self.update_results(who_is)
        if not self.standart_start(name_of_sheet, who_is):
            return
        match name_of_sheet:
            case "analytics":
                self.analytics_update()
            case "sendings":
                self.sendings_update(who_is)
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

    def analytics_update(self):
        self.choose_spreadsheetId(f"{self.who_is}-analytics")
        today = datetime.date.today()
        if today.day == 1 and today.month == 1:
            name_of_sheet = datetime.date(today.year - 1,
                                          12,
                                          calendar.monthrange(today.year - 1, 12)[1]).strftime("%b")
        elif today.day == 1:
            name_of_sheet = datetime.date(today.year,
                                          today.month - 1,
                                          calendar.monthrange(today.year, today.month - 1)[1]).strftime("%b")
        else:
            name_of_sheet = datetime.date(today.year,
                                          today.month,
                                          today.day).strftime("%b")
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

    def sendings_update(self, who_is: str):
        self.choose_spreadsheetId(f"{who_is}-sendings")

        data = self.values
        self.values = [data["keys"]]
        self.values.extend(data["main"])
        self.dist = len(self.values)

        new_or_not = self.choose_name_of_sheet("main", who_is)
        if new_or_not == 'error':
            return
        if new_or_not:
            self.create_sheet(name_of_sheet="main")
        else:
            self.update_sheet(name_of_sheet="main")

        self.values = [data["products_keys"]]
        self.values.extend(data["products"])
        self.dist = len(self.values)

        new_or_not = self.choose_name_of_sheet("products", who_is)
        if new_or_not == 'error':
            return
        if new_or_not:
            self.create_sheet(name_of_sheet="products")
        else:
            self.update_sheet(name_of_sheet="products")

        self.values = [data["financial_products_keys"]]
        self.values.extend(data["financial_products"])
        self.dist = len(self.values)

        new_or_not = self.choose_name_of_sheet("financials", who_is)
        if new_or_not == 'error':
            return
        if new_or_not:
            self.create_sheet(name_of_sheet="financials")
        else:
            self.update_sheet(name_of_sheet="financials")

    def choose_spreadsheetId(self, who_is: str):
        """
        Записывает в self.spreadsheetId Id Таблицы, с которой надо будет работать.
        :param who_is:
        :return:
        """
        self.spreadsheetId = os.getenv(f"Ozon-spreadsheetid-{who_is}")

    def start_work_with_request(self, name_of_sheet: str, who_is: str):
        request_ozon = RequestOzon(self.LockOzonRequest).start(name_of_sheet, who_is)
        if type(request_ozon) is not pandas.DataFrame:
            match request_ozon:
                case 'Missing json file':
                    self.logger.warning("Не получен файл с Ozon - start_work_with_request")
                    time.sleep(self.wait_time)
                    return self.start_work_with_request(name_of_sheet, who_is)
                case 'Проблема с соединением':
                    self.logger.warning("Проблема с соединением - RequestOzon - start_work_with_request")
                    time.sleep(self.wait_time)
                    return self.start_work_with_request(name_of_sheet, who_is)

        if request_ozon is tuple:
            if request_ozon[0] is int and request_ozon[0] != 200:
                self.result = f'ERROR: {request_ozon[1]}'
                return False
        try:
            json_response = request_ozon
        except TypeError:
            self.logger.warning("Нет доступа к файлу - start_work_with_request")
            return False

        result = self.convert_to_list(json_response, name_of_sheet, who_is)
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
