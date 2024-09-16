import datetime
import http.client
import socket
import ssl
import sys
import threading
import time
import googleapiclient.errors
import httplib2
import csv
import os


class GoogleMainFunctions:
    def __init__(self, **kwargs: threading.RLock):
        self.logger = None

        self.spreadsheetId = None
        self.service = None
        self.values, self.dist, self.needed_keys = None, None, None
        self.result = None
        self.name_of_sheet = None
        self.who_is = None

        self.lock_Google = kwargs["lock_Google"]
        self.seconds_of_lock_Google = 1.5

    def choose_name_of_sheet(self, name_of_sheet, who_is) -> bool | str:
        """
        Определяет, нужен ли создать новый лист или нет.

        P.S. Не читать код, пожалеете =)
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return: Возващает bool ответ результата определения
        """
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google - choose_name_of_sheet - {err}')
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except httplib2.error.ServerNotFoundError:
            self.logger.warning('Проблема с соединением (httplib)')
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, str(sheet_id)])
        # with open('plugins/Wildberries/data/sheets.txt', 'w', encoding="UTF-8") as txt:
        #     txt.write('\n'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes))))
        os.environ[f"sheetIDs-{who_is}"] = ';'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes)))
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

    def private_create(self, name_of_sheet: str) -> bool:
        """
        Функция, создающая лист под названием name_of_sheet.

        ВНИМАНИЕ!!! Не следует создавать лист при наличии листа с тем же названием. Не известны последствия
        :param name_of_sheet: Название листа
        :return: Возвращает bool ответ результата создания
        """
        columnCount = len(self.values[0])  # кол-во столбцов
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
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google - private_create')
            return self.private_create(name_of_sheet)
        except TimeoutError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_create(name_of_sheet)
        except ssl.SSLError as err:
            time.sleep(2)
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_create(name_of_sheet)
        except OSError as err:
            time.sleep(2)
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_create(name_of_sheet)
        except http.client.ResponseNotReady as err:
            time.sleep(2)
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_create(name_of_sheet)
        except Exception as err:
            time.sleep(2)
            self.logger.error(f"Ошибка: {err}")
            return self.private_create(name_of_sheet)
        self.logger.debug(f"Created new sheet '{name_of_sheet}'")
        self.choose_name_of_sheet(name_of_sheet=name_of_sheet, who_is=self.who_is)
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
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google - private_clear')
            return self.private_clear(name_of_sheet)
        except TimeoutError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_clear(name_of_sheet)
        except ssl.SSLError as err:
            time.sleep(2)
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_clear(name_of_sheet)
        except OSError as err:
            time.sleep(2)
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_clear(name_of_sheet)
        except http.client.ResponseNotReady as err:
            time.sleep(2)
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_clear(name_of_sheet)
        except Exception as err:
            time.sleep(2)
            self.logger.error(f"Ошибка: {err}")
            return self.private_clear(name_of_sheet)
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
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google - private_update')
            return self.private_update(name_of_sheet)
        except TimeoutError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_update(name_of_sheet)
        except ssl.SSLError as err:
            time.sleep(2)
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_update(name_of_sheet)
        except OSError as err:
            time.sleep(2)
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_update(name_of_sheet)
        except http.client.ResponseNotReady as err:
            time.sleep(2)
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_update(name_of_sheet)
        except Exception as err:
            time.sleep(2)
            self.logger.error(f"Ошибка: {err}")
            return self.private_update(name_of_sheet)
        self.logger.debug(f"Updating complete ({self.name_of_sheet})")
        self.change_formats(needed_keys=self.needed_keys, name_of_sheet=name_of_sheet)
        return False

    def change_formats(self, needed_keys: list | None, name_of_sheet: str):
        """
        При наличии столбцов, требующих изменения формата на число с двумя знаками посе запятой, функция изменяет
        формат конкретно этих столбцов.
        :param needed_keys: Список индексов столбцов
        :param name_of_sheet: Название листа, в котором работаем
        :return:
        """
        # with self.LockWbFile_ChangeFormats:
        #     with open('plugins/Wildberries/data/sheets.txt', 'r', encoding="UTF-8") as txt:
        #         data = txt.read()
        #         sheets = dict(map(lambda x: x.split('='), data.split('\n')))
        #         sheetId = sheets[name_of_sheet]
        match self.name_of_sheet:
            case "statements":
                sheets = dict(map(lambda x: x.split("="), os.getenv(f"sheetIDs-{self.who_is}-statements").split(";")))
            case "analytics":
                sheets = dict(map(lambda x: x.split("="), os.getenv(f"sheetIDs-{self.who_is}-analytics").split(";")))
            case _:
                sheets = dict(map(lambda x: x.split("="), os.getenv(f"sheetIDs-{self.who_is}").split(";")))
        sheetId = sheets[name_of_sheet]
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
        if data["requests"] == []:
            return
        try:
            getted = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=data).execute()
        except googleapiclient.errors.HttpError as err:
            time.sleep(2)
            self.logger.warning(f'Проблема с соединением Google - change_formats - {err}')
            return self.change_formats(needed_keys, name_of_sheet)
        except TimeoutError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.change_formats(needed_keys, name_of_sheet)
        except ssl.SSLError as err:
            time.sleep(2)
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.change_formats(needed_keys, name_of_sheet)
        except OSError as err:
            time.sleep(2)
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.change_formats(needed_keys, name_of_sheet)
        except http.client.ResponseNotReady as err:
            time.sleep(2)
            self.logger.warning(f'Проблема с http: {err}')
            return self.change_formats(needed_keys, name_of_sheet)
        except Exception as err:
            time.sleep(2)
            self.logger.error(f"Ошибка: {err}")
            return self.change_formats(needed_keys, name_of_sheet)

    def create_result(self, design):
        """
        При отсутствии листа Result создаёт таковой по макету в параметре design.
        :param design: Таблица, которую нужно вставить при создании
        :return:
        """
        try:
            match self.name_of_sheet:
                case "statements":
                    check = dict(
                        map(
                            lambda x: x.split('='), os.getenv(f"sheetIDs-{self.who_is}-statements").split(';')
                        )
                    )['Result']
                case "analytics":
                    check = dict(
                        map(
                            lambda x: x.split('='), os.getenv(f"sheetIDs-{self.who_is}-analytics").split(';')
                        )
                    )['Result']
                case _:
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
                time.sleep(2)
                self.logger.warning('Проблема с соединением Google - create_result')
                return self.create_result(design)
            except TimeoutError:
                time.sleep(2)
                self.logger.warning('Проблема с соединением Google (TimeoutError)')
                return self.create_result(design)
            except ssl.SSLError as err:
                time.sleep(2)
                self.logger.warning(f'Ужасная ошибка ssl: {err}')
                return self.create_result(design)
            except OSError as err:
                time.sleep(2)
                self.logger.warning(f'Вероятно TimeOutError: {err}')
                return self.create_result(design)
            except http.client.ResponseNotReady as err:
                time.sleep(2)
                self.logger.warning(f'Проблема с http: {err}')
                return self.create_result(design)
            except Exception as err:
                time.sleep(2)
                self.logger.error(f"Ошибка: {err}")
                return self.create_result(design)
            self.insert_design_result(design)

    def insert_design_result(self, design: list) -> None:
        try:
            getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "Result!A:E",
                     "majorDimension": "ROWS",
                     "values": design
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google - insert_result')
            return self.insert_design_result(design)
        except TimeoutError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.insert_design_result(design)
        except ssl.SSLError as err:
            time.sleep(2)
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.insert_design_result(design)
        except OSError as err:
            time.sleep(2)
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.insert_design_result(design)
        except http.client.ResponseNotReady as err:
            time.sleep(2)
            self.logger.warning(f'Проблема с http: {err}')
            return self.insert_design_result(design)
        except Exception as err:
            time.sleep(2)
            self.logger.error(f"Ошибка: {err}")
            return self.insert_design_result(design)
    
    def insert_new_info(self, design: list):
        if self.result == None:
            values = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Успешно записано строк: {self.dist}"]
        else:
            values = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{self.result}"]

        row = str(list(map(lambda x: x[0], design)).index(self.name_of_sheet) + 1)
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        try:
            getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                "valueInputOption": valueInputOption,
                "data": [
                    {"range": f"Result!D{row}:E{row}",
                     "majorDimension": majorDimension,
                     "values": [values]
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google - start_work_with_list_result')
            return self.insert_new_info(design)
        except TimeoutError:
            time.sleep(2)
            self.logger.warning('Проблема с соединением Google (TimeoutError) - start_work_with_list_result')
            return self.insert_new_info(design)
        except ssl.SSLError as err:
            time.sleep(2)
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.insert_new_info(design)
        except OSError as err:
            time.sleep(2)
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.insert_new_info(design)
        except http.client.ResponseNotReady as err:
            time.sleep(2)
            self.logger.warning(f'Проблема с http: {err}')
            return self.insert_new_info(design)
        except Exception as err:
            time.sleep(2)
            self.logger.error(f"Ошибка: {err}")
            return self.insert_new_info(design)

    def update_Results(self, who_is: str):
        design = list()
        match who_is:
            case "WB":
                with open('plugins/Wildberries/data/info_about_Result.csv', 'r', encoding='UTF-8') as file:
                    csv_file = csv.reader(file)
                    for row in csv_file:
                        if row == "":
                            continue
                        else:
                            design.append(row)
                users = ["grand", "terehov", "dnk", "planeta"]
            case "Ozon":
                with open('plugins/Wildberries/data/info_about_Result.csv', 'r', encoding='UTF-8') as file:
                    csv_file = csv.reader(file)
                    for row in csv_file:
                        if row == "":
                            continue
                        else:
                            design.append(row)
                users = ["grand", "terehov", "dnk"]
            case _:
                sys.exit("Wrong 'who_is' in update_Results")

        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка`
        for user in users:
            spreadsheetId = os.getenv(user)
            try:
                getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
                    "valueInputOption": valueInputOption,
                    "data": [
                        {"range": f"Result!A:E",
                         "majorDimension": majorDimension,
                         "values": design
                         }
                    ]
                }).execute()
            except googleapiclient.errors.HttpError:
                time.sleep(2)
                self.logger.warning('Проблема с соединением Google - update_Results')
                return self.update_Results()
            except TimeoutError:
                time.sleep(2)
                self.logger.warning('Проблема с соединением Google (TimeoutError) - update_Results')
                return self.update_Results()
            except ssl.SSLError as err:
                time.sleep(2)
                self.logger.warning(f'Ужасная ошибка ssl: {err}')
                return self.update_Results()
            except OSError as err:
                time.sleep(2)
                self.logger.warning(f'Вероятно TimeOutError: {err}')
                return self.update_Results()
            except http.client.ResponseNotReady as err:
                time.sleep(2)
                self.logger.warning(f'Проблема с http: {err}')
                return self.update_Results()
            except Exception as err:
                time.sleep(2)
                self.logger.error(f"Ошибка: {err}")
                return self.update_Results()
