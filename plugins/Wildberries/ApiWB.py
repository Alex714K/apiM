import datetime
import http.client
import os
import ssl
import time
import csv
from threading import Lock

import googleapiclient.errors
import googleapiclient.discovery
from plugins.Wildberries.Converter_to_list_WB import Converter
from plugins.Wildberries.Request_wildberries import RequestWildberries
from logging import getLogger
from plugins.google_main_functions import GoogleMainFunctions
from plugins.navigation.ClientEnum import Client
from plugins.navigation.NameOfSheetEnum import NameOfSheet


class ApiWB(Converter, GoogleMainFunctions):
    def __init__(self, get_service, read_lock: Lock, write_lock: Lock):
        super().__init__(get_service, read_lock, write_lock)
        self.wait_time = 3  # в секундах
        self.values = None
        self.needed_keys = None
        self.result = None
        self.name_of_sheet = None
        self.who_is = None
        self.folder = "WB"
        # self.LockWbRequest = kwargs["LockWbRequest"]
        # self.LockWbResult = kwargs["LockWbResult"]
        # self.LockWbFile_ChangeFormats = kwargs["LockWbFile_ChangeFormats"]
        self.logger = getLogger(self.__class__.__name__)

    def execute(self, who_is: Client, name_of_sheet: NameOfSheet):
        """
        Запуск работы с запросом на сервера WildBerries.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return:
        """
        self.logger.info(f"Started: folder=WB, who_is={who_is}, name_of_sheet={name_of_sheet}")
        if name_of_sheet == "update_Results":
            self.update_results(who_is)
            return
        if not self.standart_start(name_of_sheet, who_is):
            return
        match name_of_sheet:
            case "statements":
                self.statements_update(who_is)
            case "nm_report":
                self.nm_report_update(who_is)
            case _:
                self.standart_update(name_of_sheet, who_is)

    def standart_start(self, name_of_sheet: NameOfSheet, who_is: Client):
        self.name_of_sheet = name_of_sheet
        self.who_is = who_is
        if not self.start_work_with_request(name_of_sheet, who_is):
            return False
        else:
            return True

    def standart_update(self, name_of_sheet: NameOfSheet, who_is: Client):
        if len(self.values) == 0:
            return
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

    def statements_update(self, who_is):
        self.choose_spreadsheetId(who_is=f"{who_is}-statements")
        self.choose_name_of_sheet("statements", f"{self.who_is}-statements")

        # if new_or_not:
        # if self.private_create(name_of_sheet):
        #     check = False
        check1 = True
        if self.private_update_statements():
            check1 = False
        if check1:
            self.start_work_with_list_result(name_of_sheet="statements")
        elif self.result is not None:
            self.start_work_with_list_result(name_of_sheet="statements", bad=True)
        else:
            self.start_work_with_list_result(name_of_sheet="statements", bad=True)

    def choose_spreadsheetId(self, who_is: str):
        """
        Записывает в self.spreadsheetId Id Таблицы, с которой надо будет работать.
        :param who_is:
        :return:
        """
        self.spreadsheet_id = os.getenv(f"Wildberries-spreadsheetid-{who_is}")

    def start_work_with_request(self, name_of_sheet: str, who_is: str) -> bool:
        """
        Функция, в которой посылается и обрабатывается запрос на сервера WildBerries. Обработка зависит от
        названия name_of_sheet.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return: Возвращается bool ответ результата запроса
        """
        request_wb = RequestWildberries().start(name_of_sheet=name_of_sheet, who_is=who_is)
        match request_wb:
            case 'Missing json file':
                time.sleep(self.wait_time)
                return self.start_work_with_request(name_of_sheet, who_is)
            case 'Проблема с соединением':
                time.sleep(self.wait_time)
                return self.start_work_with_request(name_of_sheet, who_is)
        if request_wb[0] is int and request_wb[0] != 200:
            self.result = f'ERROR: {request_wb[1]}'
            return False
        try:
            json_response, _ = request_wb
        except TypeError:
            self.logger.warning("Нет доступа к файлу")
            return False
        try:
            result = self.convert_to_list(json_response, name_of_sheet)
        except TypeError as ex:
            self.logger.warning(ex)
            return self.start_work_with_request(name_of_sheet, who_is)

        match result:
            case 'download':
                self.logger.info(f"Downloaded {name_of_sheet}")
                self.result = 'Зачем-то скачен файл'
                return False
            case 'is None':
                self.logger.warning(f"File({self.name_of_sheet}) = None")
                self.result = 'ERROR: File=None'
                return False
            case 'is empty':
                self.logger.warning(f"File({self.name_of_sheet}) is empty ({self.who_is})")
                self.result = 'ERROR: File is empty'
                return False
        self.values, self.needed_keys = result
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
        design = list()
        with open('plugins/Wildberries/data/info_about_Result.csv', 'r', encoding='UTF-8') as file:
            csv_file = csv.reader(file)
            for row in csv_file:
                if row == "":
                    continue
                else:
                    design.append(row)
        self.create_result(design)
        self.insert_new_info(design)

    def private_update_statements(self):
        last_week = (datetime.date.today() - datetime.timedelta(days=7)).isocalendar()[1]
        try:
            self.get_service().spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id,
                                                       range=last_week
                                                       ).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google - priv_update_statements1 - {err}')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.private_update_statements()
        last_week = (datetime.date.today() - datetime.timedelta(days=7)).isocalendar()[1]
        time.sleep(5)
        try:
            self.get_service().spreadsheets().values().batchUpdate(
                spreadsheetId='1Hv0Pk6pRYN4bB5vJEdGnELmAPpXo0r25KatPCtCA_TE', body={
                    "valueInputOption": 'USER_ENTERED',
                    "data": [
                        {"range": str(last_week),
                         "majorDimension": 'ROWS',
                         "values": self.values
                         }
                    ]
                }).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google - priv_update_statements2 ({err})')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.private_update_statements()
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.private_update_statements()
        return False

    def nm_report_update(self, who_is: str):
        # В разработке
        pass
