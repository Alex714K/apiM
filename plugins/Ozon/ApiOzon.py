import datetime
import http.client
import socket
import ssl
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
    def __init__(self, service: googleapiclient.discovery.build, **kwargs):
        super().__init__()
        self.service = service
        self.values, self.dist, self.needed_keys = None, None, None
        self.result = None
        self.name_of_sheet = None
        self.who_is = None
        self.folder = None
        self.LockOzonRequest = kwargs["LockOzonRequest"]
        self.LockOzonResult = kwargs["LockOzonResult"]
        self.LockOzonFile_ChangeFormats = kwargs["LockOzonFile_ChangeFormats"]
        self.lock_Google = kwargs["lock_Google"]
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
        self.folder = folder
        if self.standart_start(name_of_sheet, who_is):
            return
        match name_of_sheet:
            case 'analytics':
                self.analytics_update(who_is)
            case _:
                self.standart_update(name_of_sheet, who_is)

    def standart_start(self, name_of_sheet: str, who_is: str):
        self.name_of_sheet = name_of_sheet
        self.who_is = who_is
        # if not self.connect_to_Google():
        #     return True
        if self.start_work_with_request(name_of_sheet, who_is):
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
        name_of_sheet = datetime.date.today().strftime("%b")
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
                return True
            case 'Проблема с соединением':
                self.logger.warning("Проблема с соединением - RequestOzon - start_work_with_request")
                self.result = 'ERROR: Проблема с соединением'
                return True
        if type(requestOzon) == tuple:
            if type(requestOzon[0]) == int and requestOzon[0] != 200:
                self.result = f'ERROR: {requestOzon[1]}'
                return True
        try:
            json_response = requestOzon
        except TypeError:
            self.logger.warning(f"Нет доступа к файлу - start_work_with_request")
            # print(f"Нет доступа к файлу ({self.name_of_sheet})")
            return True
        result = self.convert_to_list(json_response, name_of_sheet)
        match result:
            case 'download':
                self.logger.info(f"Downloaded {name_of_sheet} - start_work_with_request")
                self.result = 'Зачем-то скачен файл'
                return True
            case 'is None':
                self.logger.warning(f"File({self.name_of_sheet}) = None - start_work_with_request")
                self.result = 'ERROR: File=None'
                return True
            case 'is empty':
                self.logger.warning(f"File({self.name_of_sheet}) is empty - start_work_with_request")
                self.result = 'ERROR: File is empty'
                return True
        self.values, self.dist, self.needed_keys = result
        return False

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
        self.create_result()
        # try:
        #     getted = self.service.spreadsheets().values().batchGet(
        #         spreadsheetId=self.spreadsheetId,
        #         ranges="Result!A:E",
        #         valueRenderOption='FORMATTED_VALUE',
        #         dateTimeRenderOption='FORMATTED_STRING'
        #     ).execute()
        # except googleapiclient.errors.HttpError:
        #     self.logger.warning('Проблема с соединением Google - start_work_with_list_result')
        #     self.LockOzonResult.release()
        #     self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        #     return
        # except TimeoutError:
        #     self.logger.warning('Проблема с соединением Google (TimeoutError) - start_work_with_list_result')
        #     self.LockOzonResult.release()
        #     self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        #     return
        design_of_result = []
        with open("plugins/Ozon/data/info_about_Result_Ozon.csv", encoding="UTF-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if '' == row:
                    continue
                else:
                    design_of_result.append(row)
        # try:
        #     values = getted['valueRanges'][0]['values']
        # except KeyError:
        #     self.LockOzonResult.release()
        #     self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        #     return
        # очистка от лишних пустых элементов списка (а они бывают)
        for i in range(len(design_of_result)):
            if '' in design_of_result[i]:
                design_of_result[i] = design_of_result[i][:design_of_result[i].index('')]
        try:
            ind = (list(map(lambda x: x[0], design_of_result))).index(name_of_sheet)
        except ValueError:
            design_of_result.append(
                [name_of_sheet, '?', '?', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{self.result}"])
        else:
            if bad:
                if len(design_of_result[ind]) == 4:
                    design_of_result[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    design_of_result[ind].extend(f"{self.result}")
                elif len(design_of_result[ind]) > 4:
                    design_of_result[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    design_of_result[ind][4] = f"{self.result}"
                else:
                    design_of_result[ind].extend(
                        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{self.result}"])
            else:
                if len(design_of_result[ind]) == 4:
                    design_of_result[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    design_of_result[ind].extend(f"Успешно записано строк: {self.dist}")
                elif len(design_of_result[ind]) > 4:
                    design_of_result[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    design_of_result[ind][4] = f"Успешно записано строк: {self.dist}"
                else:
                    design_of_result[ind].extend([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        f"Успешно записано строк: {self.dist}"])

        # with open('data/info_about_Result.csv', 'w') as file:
        #     csv_file = csv.writer(file, lineterminator='\r')
        #     csv_file.writerows(ans)

        # self.private_clear(name_of_sheet="Result!A:E")

        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        try:
            getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                "valueInputOption": valueInputOption,
                "data": [
                    {"range": "Result!A:E",
                     "majorDimension": majorDimension,
                     "values": design_of_result
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google - start_work_with_list_result')
            self.LockOzonResult.release()
            return self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError) - start_work_with_list_result')
            self.LockOzonResult.release()
            return self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            self.LockOzonResult.release()
            return self.start_work_with_list_result(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            self.LockOzonResult.release()
            return self.start_work_with_list_result(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            self.LockOzonResult.release()
            return self.start_work_with_list_result(name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            self.LockOzonResult.release()
            return self.start_work_with_list_result(name_of_sheet )
        self.LockOzonResult.release()

    def create_result(self) -> None:
        """
        При отсутствии листа Result создаёт таковой по макету.
        :return:
        """
        try:
            if self.name_of_sheet == 'analytics':
                check = dict(
                    map(
                        lambda x: x.split('='), os.getenv(f"sheetIDs-{self.who_is}-analytics").split(';')
                    )
                )['Result']
            else:
                check = dict(map(lambda x: x.split('='), os.getenv(f"sheetIDs-{self.who_is}").split(';')))['Result']
        except KeyError:
            try:
                getted = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                    "requests": [{
                        "addSheet": {
                            "properties": {
                                "title": "Result",
                                "gridProperties": {
                                    "rowCount": 100,
                                    "columnCount": 26
                                }
                            }
                        }
                    }]
                }).execute()
            except googleapiclient.errors.HttpError:
                self.logger.warning('Проблема с соединением Google - create_result')
                return self.create_result()
            except TimeoutError:
                self.logger.warning('Проблема с соединением Google (TimeoutError) - create_result')
                return self.create_result()
            except ssl.SSLError as err:
                self.logger.warning(f'Ужасная ошибка ssl: {err}')
                return self.create_result()
            except OSError as err:
                self.logger.warning(f'Вероятно TimeOutError: {err}')
                return self.create_result()
            except http.client.ResponseNotReady as err:
                self.logger.warning(f'Проблема с http: {err}')
                return self.create_result()
            except Exception as err:
                self.logger.error(f"Ошибка: {err}")
                return self.create_result()
        values = list()
        with open('plugins/Ozon/data/info_about_Result_Ozon.csv', 'r', encoding='UTF-8') as file:
            csv_file = csv.reader(file)
            for i in csv_file:
                if '' == i:
                    continue
                else:
                    values.append(i)
        self.insert_design_result(values)

    def insert_design_result(self, values: list) -> None:
        try:
            getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "Result!A:E",
                     "majorDimension": "ROWS",
                     "values": values
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google - insert_design_result')
            return self.insert_design_result(values)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError) - insert_design_result')
            return self.insert_design_result(values)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.insert_design_result(values)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.insert_design_result(values)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.insert_design_result(values)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.insert_design_result(values)
