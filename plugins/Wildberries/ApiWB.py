import datetime
import http.client
import os
import socket
import ssl
import time
import googleapiclient.errors
import googleapiclient.discovery
import csv
from plugins.Wildberries.Converter_to_list_WB import Converter
from plugins.Wildberries.Request_wildberries import RequestWildberries
from logging import getLogger
from plugins.google_main_functions import GoogleMainFunctions


class ApiWB(Converter, GoogleMainFunctions):
    def __init__(self, service: googleapiclient.discovery.build, **kwargs):
        super().__init__()
        self.spreadsheetId = None
        self.service = service
        self.values, self.dist, self.needed_keys = None, None, None
        self.result = None
        self.name_of_sheet = None
        self.who_is = None
        self.LockWbRequest = kwargs["LockWbRequest"]
        self.LockWbResult = kwargs["LockWbResult"]
        self.LockWbFile_ChangeFormats = kwargs["LockWbFile_ChangeFormats"]
        self.lock_Google = kwargs["lock_Google"]
        self.logger = getLogger("ApiWB")

    def start(self, name_of_sheet: str, who_is: str, folder: str):
        """
        Запуск работы с запросом на сервера WildBerries.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :param folder: В какую папку идти
        :return:
        """
        self.logger.info(f"Started: folder=WB, who_is={who_is}, name_of_sheet={name_of_sheet}")
        if self.standart_start(name_of_sheet, who_is):
            return
        match name_of_sheet:
            case "statements":
                self.statements_update(who_is)
            case "nm_report":
                self.nm_report_update(who_is)
            case _:
                self.standart_update(name_of_sheet, who_is)

    def standart_start(self, name_of_sheet: str, who_is: str):
        self.name_of_sheet = name_of_sheet
        if self.start_work_with_request(name_of_sheet, who_is):
            return False
        else:
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
        self.spreadsheetId = os.getenv(f"Wildberries-spreadsheetid-{who_is}")

    def start_work_with_request(self, name_of_sheet: str, who_is: str) -> bool:
        """
        Функция, в которой посылается и обрабатывается запрос на сервера WildBerries. Обработка зависит от
        названия name_of_sheet.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return: Возвращает bool ответ результата запроса
        """
        requestWB = RequestWildberries(self.LockWbRequest).start(name_of_sheet=name_of_sheet, who_is=who_is)
        match requestWB:
            case 'Missing json file':
                self.result = 'ERROR: Не получен файл с WildBerries'
                return True
            case 'Проблема с соединением':
                self.result = 'ERROR: Проблема с соединением'
                return True
        if type(requestWB[0]) == int and requestWB[0] != 200:
            self.result = f'ERROR: {requestWB[1]}'
            return True
        try:
            json_response, status_code = requestWB
        except TypeError:
            self.logger.warning(f"Нет доступа к файлу")
            # print(f"Нет доступа к файлу ({self.name_of_sheet})")
            return True
        result = self.convert_to_list(json_response, name_of_sheet)
        match result:
            case 'download':
                self.logger.info(f"Downloaded {name_of_sheet}")
                self.result = 'Зачем-то скачен файл'
                return True
            case 'is None':
                self.logger.warning(f"File({self.name_of_sheet}) = None")
                self.result = 'ERROR: File=None'
                return True
            case 'is empty':
                self.logger.warning(f"File({self.name_of_sheet}) is empty")
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
        self.LockWbResult.acquire()
        self.create_result()
        design_of_result = []
        with open("plugins/Wildberries/data/info_about_Result.csv", encoding="UTF-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if '' == row:
                    continue
                else:
                    design_of_result.append(row)
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

        # with open('plugins/Wildberries/data/info_about_Result.csv', 'w') as file:
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
            self.logger.warning('Проблема с соединением Google - start_result2')
            self.LockWbResult.release()
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
            return
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            self.LockWbResult.release()
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
            return
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            self.LockWbResult.release()
            return self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            self.LockWbResult.release()
            return self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            self.LockWbResult.release()
            return self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            self.LockWbResult.release()
            return self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        self.LockWbResult.release()

    def create_result(self) -> None:
        """
        При отсутствии листа Result создаёт таковой по макету.
        :return:
        """
        try:
            if self.name_of_sheet == 'statements':
                check = dict(
                    map(
                        lambda x: x.split('='), os.getenv(f"sheetIDs-{self.who_is}-statements").split(';')
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
                self.logger.warning('Проблема с соединением Google (TimeoutError)')
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
        with open('plugins/Wildberries/data/info_about_Result.csv', 'r', encoding='UTF-8') as file:
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
            self.logger.warning('Проблема с соединением Google - insert_result')
            return self.insert_design_result(values)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
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

    def start_work_with_statements(self, name_of_sheet: str, who_is: str):
        self.choose_spreadsheetId(who_is=f"{who_is}-statements")
        # Кастыль, чтобы не переделывать весь код TODO Сделай нормально, блин
        self.who_is, who_is = f"{self.who_is}-statements", self.who_is
        self.choose_name_of_sheet(name_of_sheet, who_is)
        self.who_is = who_is

        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is)
        if check:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
            return
        # if new_or_not:
        # if self.private_create(name_of_sheet):
        #     check = False
        check1 = True
        if self.private_update_statements():
            check1 = False
        if check1:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        elif self.result is not None:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
        else:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)

    def private_update_statements(self):
        # getted = self.service.spreadsheets().
        # get(spreadsheetId='1Hv0Pk6pRYN4bB5vJEdGnELmAPpXo0r25KatPCtCA_TE').execute()
        # getted = getted['sheets']
        # need = list()
        # for info in getted:
        #     need.append([info['properties']['title'], info['properties']['sheetId']])
        last_week = (datetime.date.today() - datetime.timedelta(days=7)).isocalendar()[1]
        try:
            getted = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId,
                                                                range=last_week
                                                                ).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google - priv_update_statements1 - {err}')
            return self.private_update_statements()
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_update_statements()
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_update_statements()
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_update_statements()
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_update_statements()
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.private_update_statements()
        last_week = (datetime.date.today() - datetime.timedelta(days=7)).isocalendar()[1]
        try:
            getted = self.service.spreadsheets().values().batchUpdate(
                spreadsheetId='1Hv0Pk6pRYN4bB5vJEdGnELmAPpXo0r25KatPCtCA_TE', body={
                    "valueInputOption": 'USER_ENTERED',
                    "data": [
                        {"range": str(last_week),
                         "majorDimension": 'ROWS',
                         "values": self.values
                         }
                    ]
                }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google - priv_update_statements2')
            return self.private_update_statements()
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_update_statements()
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_update_statements()
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_update_statements()
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_update_statements()
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.private_update_statements()
        return False

    def nm_report_update(self, who_is: str):
        pass
