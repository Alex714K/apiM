import datetime
import ssl
import threading
import time
import os
from threading import Lock

import httplib2
import http.client
import googleapiclient.errors


class GoogleMainFunctions:
    def __init__(self, get_service, read_lock: Lock, write_lock: Lock):
        self.logger = None

        self.wait_time = 1.1  # в секундах

        self.spreadsheet_id = None
        self.get_service = get_service
        self.values = None
        self.needed_keys = None
        self.result = None
        self.name_of_sheet = None
        self.who_is = None
        self.folder = None
        self.read_lock = read_lock
        self.write_lock = write_lock

    def get_sheets_names_and_indexes(self):
        # sheet_properties = dict()
        # try:
        #     with open(f"data/sheetIds/sheet_ids_{self.who_is}.csv", "r", encoding="UTF-8") as file:
        #         sheet_properties = dict(csv.reader(file, lineterminator="\n", delimiter=";"))
        # except FileNotFoundError:
        #     sheet_properties = self.get_sheets_names_and_indexes_from_google()
        #     with open(f"data/sheetIds/sheet_ids_{self.who_is}.csv", "w", encoding="UTF-8") as file:
        #         csv.writer(file, lineterminator="\n", delimiter=";").writerows(list(sheet_properties.items()))
        # except IndexError:
        #     sheet_properties = self.get_sheets_names_and_indexes_from_google()
        #     with open(f"data/sheetIds/sheet_ids_{self.who_is}.csv", "w", encoding="UTF-8") as file:
        #         csv.writer(file, lineterminator="\n", delimiter=";").writerows(list(sheet_properties.items()))

        return self.get_sheets_names_and_indexes_from_google()

    def get_sheets_names_and_indexes_from_google(self):
        self.read_lock.acquire()
        threading.Timer(self.wait_time, self.read_lock.release).start()

        try:
            sheets_metadata = self.get_service(self.folder).spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - get_sheets_metadata_from_google - {err}')
            time.sleep(self.wait_time)
            return self.get_sheets_names_and_indexes_from_google()
        except httplib2.error.ServerNotFoundError:
            self.logger.warning('Проблема с соединением (httplib)')
            time.sleep(self.wait_time)
            return self.get_sheets_names_and_indexes_from_google()
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError)')
            time.sleep(self.wait_time)
            return self.get_sheets_names_and_indexes_from_google()
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.get_sheets_names_and_indexes_from_google()
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.get_sheets_names_and_indexes_from_google()
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.get_sheets_names_and_indexes_from_google()
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.get_sheets_names_and_indexes_from_google()

        ans = list()
        for sheet_property in sheets_metadata["sheets"]:
            ans.append([sheet_property["properties"]["title"], sheet_property["properties"]["index"]])

        return ans


    def choose_name_of_sheet(self, name_of_sheet, who_is) -> bool:
        """
        Определяет, нужен ли создать новый лист или нет.

        P.S. Не читать код, пожалеете =)
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return: Возващает bool ответ результата определения
        """
        self.read_lock.acquire()
        threading.Timer(self.wait_time, self.read_lock.release).start()

        try:
            sheet_metadata = self.get_service(self.folder).spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - choose_name_of_sheet - {err}')
            time.sleep(self.wait_time)
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except httplib2.error.ServerNotFoundError:
            self.logger.warning('Проблема с соединением (httplib)')
            time.sleep(self.wait_time)
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError)')
            time.sleep(self.wait_time)
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.choose_name_of_sheet(name_of_sheet, who_is)
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, str(sheet_id)])
        os.environ[f"sheetIDs-{who_is}"] = ';'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes)))
        if name_of_sheet in list(map(lambda x: x[0], names_of_lists_and_codes)):
            return False
        return True

    def create_sheet(self, name_of_sheet: str):
        if self.private_create(name_of_sheet=name_of_sheet):
            return False
        if self.private_update(name_of_sheet=name_of_sheet):
            return False
        return True

    def update_sheet(self, name_of_sheet: str):
        if not self.private_clear(name_of_sheet=name_of_sheet):
            return False
        if not self.private_update(name_of_sheet=name_of_sheet):
            return False
        return True

    def private_create(self, name_of_sheet: str) -> bool:
        """
        Функция, создающая лист под названием name_of_sheet.

        ВНИМАНИЕ!!! Не следует создавать лист при наличии листа с тем же названием. Не известны последствия
        :param name_of_sheet: Название листа
        :return: Возвращает bool ответ результата создания
        """
        if len(self.values) == 0:
            column_count = 0
        else:
            column_count = len(self.values[0])  # кол-во столбцов

        self.write_lock.acquire()
        threading.Timer(self.wait_time, self.write_lock.release).start()

        try:
            self.get_service(self.folder).spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body={
                "requests": [{
                    "addSheet": {
                        "properties": {
                            "title": name_of_sheet,
                            "gridProperties": {
                                "rowCount": len(self.values),
                                "columnCount": column_count
                            }
                        }
                    }
                }]
            }).execute()
        except googleapiclient.errors.HttpError as ex:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - private_create - {ex}')
            time.sleep(self.wait_time)
            return self.private_create(name_of_sheet)
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError)')
            time.sleep(self.wait_time)
            return self.private_create(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.private_create(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.private_create(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.private_create(name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.private_create(name_of_sheet)
        self.logger.debug(f"Created new sheet '{name_of_sheet}' ({self.who_is})")
        self.choose_name_of_sheet(name_of_sheet=name_of_sheet, who_is=self.who_is)
        return False

    def private_clear(self, name_of_sheet: str) -> bool:
        """
        Функция, очищающая лист под название name_of_sheet
        :param name_of_sheet: Название листа
        :return: Возвращает bool ответ результата очистки
        """
        if len(self.values) == 0:
            return False
        if name_of_sheet != "Result!A:E":
            needed_letter = self.create_last_letter_from_width(len(self.values[0]))
            r = f"{name_of_sheet}!A:{needed_letter}"
        else:
            r = name_of_sheet

        self.write_lock.acquire()
        threading.Timer(self.wait_time, self.write_lock.release).start()

        try:
            self.get_service(self.folder).spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id, range=r
                                                       ).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - private_clear - {err}')
            time.sleep(self.wait_time)
            return self.private_clear(name_of_sheet)
        except TimeoutError as err:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) ({err})')
            time.sleep(self.wait_time)
            return self.private_clear(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.private_clear(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.private_clear(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.private_clear(name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.private_clear(name_of_sheet)
        self.logger.debug(f"Clearing complete (nameOfSheet: {name_of_sheet}, Client: {self.who_is})")
        return True

    @staticmethod
    def create_last_letter_from_width(dist) -> str:
        needed_letter = ""
        a_ord = ord("A")
        while True:
            if dist < 26:
                needed_letter += chr(a_ord + dist)
                break
            needed_letter += chr(a_ord + dist % 26)
            dist //= 26

        return needed_letter

    def private_update(self, name_of_sheet: str) -> bool:
        """
        Функция, обновляющий лист под название name_of_sheet.
        :param name_of_sheet: Название листа
        :return: Возвращает bool ответ результата обновления
        """
        sheet_id = self.get_sheet_id(name_of_sheet)
        difference_distance = len(self.values) - self.get_row_count_in_sheet(sheet_id)
        if difference_distance > 0:
            self.append_new_rows(sheet_id, difference_distance)

        value_input_option = "USER_ENTERED"
        major_dimension = "ROWS"  # список - строка
        self.write_lock.acquire()
        for i in range(1, len(self.values) + 1, 1000):
            distance = f"{name_of_sheet}!{i}:{i+1000}"

            try:
                self.get_service(self.folder).spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id, body={
                    "valueInputOption": value_input_option,
                    "data": [
                        {"range": distance,
                         "majorDimension": major_dimension,
                         "values": self.values[i-1:i+1000-1]
                         }
                    ]
                }).execute()
            except googleapiclient.errors.HttpError as err:
                self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - private_update - {err}')
                time.sleep(self.wait_time)
                return self.private_update(name_of_sheet)
            except TimeoutError as err:
                self.logger.warning(f'Проблема с соединением Google ({self.who_is}) ({err})')
                time.sleep(self.wait_time)
                return self.private_update(name_of_sheet)
            except ssl.SSLError as err:
                self.logger.warning(f'Ужасная ошибка ssl: {err}')
                time.sleep(self.wait_time)
                return self.private_update(name_of_sheet)
            except OSError as err:
                self.logger.warning(f'Вероятно TimeOutError: {err}')
                time.sleep(self.wait_time)
                return self.private_update(name_of_sheet)
            except http.client.ResponseNotReady as err:
                self.logger.warning(f'Проблема с http: {err}')
                time.sleep(self.wait_time)
                return self.private_update(name_of_sheet)
            except Exception as err:
                self.logger.error(f"Ошибка: {err}")
                time.sleep(self.wait_time)
                return self.private_update(name_of_sheet)

            time.sleep(self.wait_time)

        self.logger.debug(f"Updating complete (NameOfSheet: {name_of_sheet}, Client: {self.who_is})")

        self.write_lock.release()

        self.change_formats(needed_keys=self.needed_keys, name_of_sheet=name_of_sheet)
        return True

    def append_new_rows(self,sheet_id: str, num_rows: int):
        requests = [{
            "appendDimension": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "length": num_rows
            }
        }]

        body = {
            'requests': requests
        }

        self.write_lock.acquire()
        threading.Timer(self.wait_time, self.write_lock.release).start()

        try:
            response = self.get_service(self.folder).spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - change_formats - {err}')
            time.sleep(self.wait_time)
            return self.append_new_rows(sheet_id, num_rows)
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError)')
            time.sleep(self.wait_time)
            return self.append_new_rows(sheet_id, num_rows)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.append_new_rows(sheet_id, num_rows)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.append_new_rows(sheet_id, num_rows)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.append_new_rows(sheet_id, num_rows)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.append_new_rows(sheet_id, num_rows)
        self.logger.info(f"Rows of sheet '{self.name_of_sheet}' is increased ({self.who_is}).")

        return response

    def change_formats(self, needed_keys: list | None, name_of_sheet: str):
        """
        При наличии столбцов, требующих изменения формата на число с двумя знаками посе запятой, функция изменяет
        формат конкретно этих столбцов.
        :param needed_keys: Список индексов столбцов
        :param name_of_sheet: Название листа, в котором работаем
        :return:
        """
        sheet_id = self.get_sheet_id(name_of_sheet)
        if needed_keys is None:
            return None
        data = {"requests": []}
        for i in needed_keys:
            data["requests"].append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startColumnIndex": i,
                        "endColumnIndex": i + 1
                    },
                    "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}}},
                    "fields": "userEnteredFormat(numberFormat)"
                }
            })
        if not data["requests"]:
            return None

        self.write_lock.acquire()
        threading.Timer(self.wait_time, self.write_lock.release).start()

        try:
            self.get_service(self.folder).spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=data).execute()
            return None
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - change_formats - {err}')
            time.sleep(self.wait_time)
            return self.change_formats(needed_keys, name_of_sheet)
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError)')
            time.sleep(self.wait_time)
            return self.change_formats(needed_keys, name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.change_formats(needed_keys, name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.change_formats(needed_keys, name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.change_formats(needed_keys, name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.change_formats(needed_keys, name_of_sheet)

    def create_result(self, design):
        """
        При отсутствии листа Result создаёт таковой по макету в параметре design.
        :param design: Таблица, которую нужно вставить при создании
        :return:
        """
        has_result = "Result" in self.get_all_sheet_ids().keys()
        if not has_result:
            self.write_lock.acquire()
            threading.Timer(self.wait_time, self.write_lock.release).start()

            try:
                self.get_service(self.folder).spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body={
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
            except googleapiclient.errors.HttpError as ex:
                self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - create_result - {ex}')
                time.sleep(self.wait_time)
                return self.create_result(design)
            except TimeoutError:
                self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError)')
                time.sleep(self.wait_time)
                return self.create_result(design)
            except ssl.SSLError as err:
                self.logger.warning(f'Ужасная ошибка ssl: {err}')
                time.sleep(self.wait_time)
                return self.create_result(design)
            except OSError as err:
                self.logger.warning(f'Вероятно TimeOutError: {err}')
                time.sleep(self.wait_time)
                return self.create_result(design)
            except http.client.ResponseNotReady as err:
                self.logger.warning(f'Проблема с http: {err}')
                time.sleep(self.wait_time)
                return self.create_result(design)
            except Exception as err:
                self.logger.error(f"Ошибка: {err}")
                time.sleep(self.wait_time)
                return self.create_result(design)
            self.insert_design_result(design)
            self.logger.info(f"Created result (Client: {self.who_is})")
            return None
        return None

    def insert_design_result(self, design: list) -> None:
        self.write_lock.acquire()
        threading.Timer(self.wait_time, self.write_lock.release).start()

        try:
            self.get_service(self.folder).spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id, body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "Result!A:E",
                     "majorDimension": "ROWS",
                     "values": design
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - insert_result')
            time.sleep(self.wait_time)
            return self.insert_design_result(design)
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError)')
            time.sleep(self.wait_time)
            return self.insert_design_result(design)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.insert_design_result(design)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.insert_design_result(design)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.insert_design_result(design)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.insert_design_result(design)
        return None

    def insert_new_info(self, design: list):
        if self.result is None:
            values = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Успешно записано строк: {len(self.values)}"]
        else:
            values = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{self.result}"]

        row = str(list(map(lambda x: x[0], design)).index(self.name_of_sheet) + 1)
        value_input_option = "USER_ENTERED"
        major_dimension = "ROWS"  # список - строка

        self.write_lock.acquire()
        threading.Timer(self.wait_time, self.write_lock.release).start()

        try:
            self.get_service(self.folder).spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id, body={
                "valueInputOption": value_input_option,
                "data": [
                    {"range": f"Result!D{row}:E{row}",
                     "majorDimension": major_dimension,
                     "values": [values]
                     }
                ]
            }).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - start_work_with_list_result')
            time.sleep(self.wait_time)
            return self.insert_new_info(design)
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError) - start_work_with_list_result')
            time.sleep(self.wait_time)
            return self.insert_new_info(design)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.insert_new_info(design)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.insert_new_info(design)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.insert_new_info(design)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.insert_new_info(design)
        self.logger.info(f"Inserted info in Result (Client: {self.who_is})")
        return None

    def update_results(self, who_is: str):
        from plugins.test.data import UpdateAndSchedules
        import csv
        import sys

        design = list()
        match who_is:
            case "WB":
                with open('plugins/Wildberries/data/info_about_Result.csv', 'r', encoding='UTF-8') as file:
                    csv_file = csv.reader(file)
                    for row in filter(lambda x: x != "", csv_file):
                        design.append(row)
                users = UpdateAndSchedules.clients_wb
            case "Ozon":
                with open('plugins/Ozon/data/info_about_Result_Ozon.csv', 'r', encoding='UTF-8') as file:
                    csv_file = csv.reader(file)
                    for row in filter(lambda x: x != "", csv_file):
                        design.append(row)
                users = UpdateAndSchedules.clients_ozon
            case _:
                sys.exit("Wrong 'who_is' in update_Results")

        value_input_option = "USER_ENTERED"
        major_dimension = "ROWS"  # список - строка`
        for user in users:
            match who_is:
                case "WB":
                    spreadsheet_id = os.getenv(f"Wildberries-spreadsheetid-{user}")
                case "Ozon":
                    spreadsheet_id = os.getenv(f"Ozon-spreadsheetid-{user}")
                case _:
                    continue

            self.write_lock.acquire()
            threading.Timer(self.wait_time, self.write_lock.release).start()

            try:
                self.get_service(self.folder).spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body={
                    "valueInputOption": value_input_option,
                    "data": [
                        {"range": "Result!A:E",
                         "majorDimension": major_dimension,
                         "values": design
                         }
                    ]
                }).execute()
            except googleapiclient.errors.HttpError:
                self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - update_Results')
                time.sleep(self.wait_time)
                return self.update_results(who_is)
            except TimeoutError:
                self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError) - update_Results')
                time.sleep(self.wait_time)
                return self.update_results(who_is)
            except ssl.SSLError as err:
                self.logger.warning(f'Ужасная ошибка ssl: {err}')
                time.sleep(self.wait_time)
                return self.update_results(who_is)
            except OSError as err:
                self.logger.warning(f'Вероятно TimeOutError: {err}')
                time.sleep(self.wait_time)
                return self.update_results(who_is)
            except http.client.ResponseNotReady as err:
                self.logger.warning(f'Проблема с http: {err}')
                time.sleep(self.wait_time)
                return self.update_results(who_is)
            except Exception as err:
                self.logger.error(f"Ошибка: {err}")
                time.sleep(self.wait_time)
                return self.update_results(who_is)
            finally:
                self.logger.info(f"Updated {user}'s result")
                time.sleep(self.wait_time)
        self.logger.info("Updated results")

    def get_row_count_in_sheet(self, sheet_id: int | str) -> int:
        self.read_lock.acquire()
        threading.Timer(self.wait_time, self.read_lock.release).start()

        try:
            sheet_metadata = self.get_service(self.folder).spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - get_row_count_in_sheet')
            time.sleep(self.wait_time)
            return self.get_row_count_in_sheet(sheet_id)
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError) - get_row_count_in_sheet')
            time.sleep(self.wait_time)
            return self.get_row_count_in_sheet(sheet_id)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.get_row_count_in_sheet(sheet_id)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.get_row_count_in_sheet(sheet_id)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.get_row_count_in_sheet(sheet_id)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.get_row_count_in_sheet(sheet_id)

        sheets = sheet_metadata.get("sheets", "")

        is_sheet_id_int = type(sheet_id) is int
        for sheet in sheets:
            if (is_sheet_id_int and sheet_id == sheet["properties"]["sheetId"] or
                sheet_id == sheet["properties"]["title"]):
                return int(sheet["properties"]["gridProperties"]["rowCount"])
        return 0

    def get_all_sheet_ids_from_google(self) -> dict:
        ans = dict()

        self.read_lock.acquire()
        threading.Timer(self.wait_time, self.read_lock.release).start()

        try:
            sheet_metadata = self.get_service(self.folder).spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        except googleapiclient.errors.HttpError as ex:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) - get_all_sheet_ids - {ex}')
            time.sleep(self.wait_time)
            return self.get_all_sheet_ids_from_google()
        except TimeoutError:
            self.logger.warning(f'Проблема с соединением Google ({self.who_is}) (TimeoutError) - get_all_sheet_ids')
            time.sleep(self.wait_time)
            return self.get_all_sheet_ids_from_google()
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            time.sleep(self.wait_time)
            return self.get_all_sheet_ids_from_google()
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            time.sleep(self.wait_time)
            return self.get_all_sheet_ids_from_google()
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            time.sleep(self.wait_time)
            return self.get_all_sheet_ids_from_google()
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            time.sleep(self.wait_time)
            return self.get_all_sheet_ids_from_google()

        sheets = sheet_metadata.get("sheets", "")
        for sheet in sheets:
            ans[sheet["properties"]["title"]] = sheet["properties"]["sheetId"]
        return ans

    def get_all_sheet_ids(self) -> dict:
        # sheet_ids = dict()
        # try:
        #     with open(f"data/sheetIds/sheet_ids_{self.who_is}_{self.folder}.csv", "r", encoding="UTF-8") as file:
        #         sheet_ids = dict(csv.reader(file, lineterminator="\n", delimiter=";"))
        # except Exception:
        #     sheet_ids = self.get_all_sheet_ids_from_google()
        #     with open(f"data/sheetIds/sheet_ids_{self.who_is}_{self.folder}.csv", "w", encoding="UTF-8") as file:
        #         csv.writer(file, lineterminator="\n", delimiter=";").writerows(list(sheet_ids.items()))

        return self.get_all_sheet_ids_from_google()

    def get_sheet_id(self, name_of_sheet: str) -> str:
        return self.get_all_sheet_ids()[name_of_sheet]

    @staticmethod
    def replace_from_dot_to_comma(file: list | dict):
        if type(file) is dict:
            return file
        else:
            return list(map(lambda row: list(map(lambda x: str(x).replace(".", ",", 1), row)), file))
