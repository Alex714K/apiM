import datetime
import logging
import socket
import threading
import time
import googleapiclient.errors
import httplib2
from google.oauth2 import service_account
from googleapiclient.discovery import build
import csv
from plugins.Ozon.Converter_to_list_Ozon import Converter
from plugins.Ozon.Request_Ozon import RequestOzon
from logging import getLogger
import os


class ApiOzon(Converter):
    def __init__(self, lock_ozon_request: threading.RLock, lock_ozon_result: threading.RLock):
        super().__init__()
        self.spreadsheetId = None
        self.service = None
        self.values, self.dist, self.needed_keys = None, None, None
        self.result = None
        self.name_of_sheet = None
        self.lock_ozon_request = lock_ozon_request
        self.lock_ozon_result = lock_ozon_result
        self.logger = getLogger("ApiOzon")

    def start(self, name_of_sheet: str, who_is: str):
        self.logger.info(f"Started: folder=Ozon, who_is={who_is}, name_of_sheet={name_of_sheet}")
        if self.standart_start(name_of_sheet, who_is):
            return
        match name_of_sheet:
            case 'analytics':
                self.analytics_start()
            case _:
                self.standart_update(name_of_sheet, who_is)

    def standart_start(self, name_of_sheet: str, who_is: str):
        self.name_of_sheet = name_of_sheet
        if not self.connect_to_Google():
            return True
        if self.start_work_with_request(name_of_sheet, who_is):
            return True

    def standart_update(self, name_of_sheet: str, who_is: str):
        self.choose_spreadsheetId(who_is)
        new_or_not = self.choose_name_of_sheet(name_of_sheet=name_of_sheet)
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

    def analytics_start(self):
        self.choose_spreadsheetId('analytics')
        name_of_sheet = datetime.date.today().strftime("%b")
        new_or_not = self.choose_name_of_sheet(name_of_sheet=name_of_sheet)
        if new_or_not == 'error':
            return
        if new_or_not:
            check = self.create_sheet(name_of_sheet=name_of_sheet)
        else:
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
            service = build('sheets', 'v4', credentials=credentials)
        except httplib2.error.ServerNotFoundError:
            self.logger.warning(f"Google ({self.name_of_sheet}): ServerNotFound")
            time.sleep(2)
            return self.connect_to_Google()
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({self.name_of_sheet})")
            time.sleep(2)
            return self.connect_to_Google()
        finally:
            self.logger.debug(f"Connected to Google({self.name_of_sheet})")
        self.service = service
        return True

    def choose_name_of_sheet(self, name_of_sheet: str) -> bool | str:
        """
        Определяет, нужен ли создать новый лист или нет.

        P.S. Не читать код, пожалеете =)
        :param name_of_sheet: Название листа
        :return: Возващает bool | str ответ результата определения
        """
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google')
            return self.choose_name_of_sheet(name_of_sheet)
        except httplib2.error.ServerNotFoundError:
            self.logger.warning('Проблема с соединением (httplib)')
            return self.choose_name_of_sheet(name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.choose_name_of_sheet(name_of_sheet)
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, str(sheet_id)])
        with open('plugins/Ozon/data/sheets_Ozon.txt', 'w', encoding="UTF-8") as txt:
            txt.write('\n'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes))))
        if name_of_sheet in list(map(lambda x: x[0], names_of_lists_and_codes)):
            return False
        else:
            return True

    def create_sheet(self, name_of_sheet: str):
        if self.private_create(name_of_sheet=name_of_sheet):
            return False
        if self.private_update(name_of_sheet=name_of_sheet):
            return False
        return True

    def update_sheet(self, name_of_sheet: str):
        if self.private_clear(name_of_sheet=name_of_sheet):
            return False
        if self.private_update(name_of_sheet=name_of_sheet):
            return False
        return True

    def start_work_with_request(self, name_of_sheet: str, who_is: str):
        requestOzon = RequestOzon(self.lock_ozon_request).start(name_of_sheet, who_is)
        match requestOzon:
            case 'Missing json file':
                self.logger.warning("Не получен файл с Ozon")
                self.result = 'ERROR: Не получен файл с Ozon'
                return True
            case 'Проблема с соединением':
                self.logger.warning("Проблема с соединением - RequestOzon")
                self.result = 'ERROR: Проблема с соединением'
                return True
        if type(requestOzon[0]) == int and requestOzon[0] != 200:
            self.result = f'ERROR: {requestOzon[1]}'
            return True
        try:
            json_response = requestOzon
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

    def private_create(self, name_of_sheet: str) -> bool:
        """
        Функция, создающая лист под названием name_of_sheet.

        ВНИМАНИЕ!!! Не следует создавать лист при наличии листа с тем же названием. Не известны последствия
        :param name_of_sheet: Название листа
        :return: Возвращает bool ответ результата создания
        """
        columnCount = len(self.values[0])  # кол-во столбцов
        name_of_sheet = name_of_sheet
        try:
            getted = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                "requests": [{
                    "addSheet": {
                        "properties": {
                            "title": name_of_sheet,
                            "gridProperties": {
                                "rowCount": self.dist,
                                "columnCount": columnCount
                            }
                        }
                    }
                }]
            }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google')
            return True
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return True
        self.logger.debug(f"Created new sheet '{name_of_sheet}'")
        # print(f"\nCreated new sheet '{name_of_sheet}'")
        self.choose_name_of_sheet(name_of_sheet=name_of_sheet)
        return False

    def private_clear(self, name_of_sheet: str) -> bool:
        """
        Функция, очищающая лист под название name_of_sheet
        :param name_of_sheet: Название листа
        :return: Возвращает bool ответ результата очистки
        """
        if name_of_sheet != "Result!A:E":
            dist = len(self.values[0])
            if dist % 26 == 0:
                needed_letter = chr(ord('A') + 26 - 1)
            else:
                needed_letter = chr(ord('A') + dist % 26 - 1)
            if dist > 26 and dist % 26 == 0:
                needed_letter = f"{chr(ord("A") - 1 + (dist // 26 - 1))}{needed_letter}"
            elif dist > 26:
                needed_letter = f"{chr(ord("A") - 1 + (dist // 26))}{needed_letter}"
            r = f"{name_of_sheet}!A:{needed_letter}"
        else:
            r = name_of_sheet
        try:
            getted = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=r
                                                                ).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google')
            return True
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return True
        self.logger.debug(f"Clearing complete ({name_of_sheet})")
        return False

    def private_update(self, name_of_sheet: str) -> bool:
        """
        Функция, обновляющий лист под название name_of_sheet.
        :param name_of_sheet: Название листа
        :return: Возвращает bool ответ результата обновления
        """
        distance = f"{name_of_sheet}"
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        try:
            getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                "valueInputOption": valueInputOption,
                "data": [
                    {"range": distance,
                     "majorDimension": majorDimension,
                     "values": self.values
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google')
            return True
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return True
        self.logger.debug(f"Updating complete ({self.name_of_sheet})")
        with open('plugins/Ozon/data/sheets_Ozon.txt', 'r', encoding="UTF-8") as txt:
            self.logger.debug(f"sheet_ids:{print(txt.read().split('\n'))}")
            sheets = dict(map(lambda x: x.split('='), txt.read().split('\n')))
            sheetId = sheets[name_of_sheet]
        self.change_formats(needed_keys=self.needed_keys, sheetId=sheetId)
        return False

    def change_formats(self, needed_keys: list | None, sheetId: str):
        """
        При наличии столбцов, требующих изменения формата на число с двумя знаками посе запятой, функция изменяет
        формат конкретно этих столбцов.
        :param needed_keys: Список индексов столбцов
        :param sheetId: Id листа, в котором работаем
        :return:
        """
        if needed_keys == None:
            return
        data = {"requests": []}
        for i in needed_keys:
            data["requests"].append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheetId,
                        "startColumnIndex": i,
                        "endColumnIndex": i + 1
                    },
                    "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}}},
                    "fields": "userEnteredFormat(numberFormat)"
                }
            })
        try:
            getted = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=data).execute()
        except googleapiclient.errors.HttpError:
            self.result = 'ERROR: Проблема с соединением'
            return False
        except TimeoutError:
            self.result = 'ERROR: Проблема с соединением (TimeoutError)'
            self.logger.critical('Попытка установить соединение была безуспешной (с Google)')
            return False
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
        self.lock_ozon_result.acquire()
        self.create_result()
        try:
            getted = self.service.spreadsheets().values().batchGet(
                spreadsheetId=self.spreadsheetId,
                ranges="Result!A:E",
                valueRenderOption='FORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING'
            ).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google')
            self.lock_ozon_result.release()
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
            return
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            self.lock_ozon_result.release()
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
            return
        try:
            values = getted['valueRanges'][0]['values']
        except KeyError:
            self.lock_ozon_result.release()
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
            return
        # очистка от лишних пустых элементов списка (а они бывают)
        for i in range(len(values)):
            if '' in values[i]:
                values[i] = values[i][:values[i].index('')]
        try:
            ind = (list(map(lambda x: x[0], values))).index(name_of_sheet)
        except ValueError:
            values.append(
                [name_of_sheet, '?', '?', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{self.result}"])
        else:
            if bad:
                if len(values[ind]) == 4:
                    values[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    values[ind].extend(f"{self.result}")
                elif len(values[ind]) > 4:
                    values[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    values[ind][4] = f"{self.result}"
                else:
                    values[ind].extend(
                        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{self.result}"])
            else:
                if len(values[ind]) == 4:
                    values[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    values[ind].extend(f"Успешно записано строк: {self.dist}")
                elif len(values[ind]) > 4:
                    values[ind][3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    values[ind][4] = f"Успешно записано строк: {self.dist}"
                else:
                    values[ind].extend([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        f"Успешно записано строк: {self.dist}"])

        # with open('data/info_about_Result.csv', 'w') as file:
        #     csv_file = csv.writer(file, lineterminator='\r')
        #     csv_file.writerows(ans)

        self.private_clear(name_of_sheet="Result!A:E")

        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        try:
            getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                "valueInputOption": valueInputOption,
                "data": [
                    {"range": "Result!A:E",
                     "majorDimension": majorDimension,
                     "values": values
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google')
            self.lock_ozon_result.release()
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
            return
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            self.lock_ozon_result.release()
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
            return
        self.lock_ozon_result.release()

    def create_result(self) -> None:
        """
        При отсутствии листа Result создаёт таковой по макету.
        :return:
        """
        with open('plugins/Ozon/data/sheets_Ozon.txt', 'r', encoding="UTF-8") as txt:
            try:
                check = dict(map(lambda x: x.split('='), txt.read().split('\n')))['Result']
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
                    self.logger.warning('Проблема с соединением Google')
                    return self.create_result()
                except TimeoutError:
                    self.logger.warning('Проблема с соединением Google (TimeoutError)')
                    return self.create_result()
                self.insert_design_result()

    def insert_design_result(self) -> None:
        values = list()
        with open('plugins/Ozon/data/info_about_Result_Ozon.csv', 'r', encoding='UTF-8') as file:
            csv_file = csv.reader(file)
            for i in csv_file:
                if '' == i:
                    continue
                else:
                    values.append(i)
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
            self.logger.warning('Проблема с соединением Google')
            return self.insert_design_result()
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.insert_design_result()
