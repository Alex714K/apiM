import datetime
import http.client
import os
import socket
import ssl
import time
import googleapiclient.errors
import httplib2
from google.oauth2 import service_account
import googleapiclient.discovery
import csv
from plugins.Wildberries.Converter_to_list_WB import Converter
from plugins.Wildberries.Request_wildberries import RequestWildberries
from logging import getLogger


class ApiWB(Converter):
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

    def start(self, name_of_sheet: str, who_is: str):
        """
        Запуск работы с запросом на сервера WildBerries.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return:
        """
        self.logger.info(f"Started: folder=WB, who_is={who_is}, name_of_sheet={name_of_sheet}")
        self.name_of_sheet = name_of_sheet
        self.who_is = who_is
        if name_of_sheet == 'nm_report':
            return self.nm_report(who_is)
        self.choose_spreadsheetId(who_is=who_is)
        # if not self.connect_to_Google():
        #     return
        if name_of_sheet == 'statements':
            self.start_work_with_statements(name_of_sheet=name_of_sheet, who_is=who_is)
            return
        new_or_not = self.choose_name_of_sheet(name_of_sheet=name_of_sheet)
        if new_or_not == 'error':
            return
        if new_or_not:
            check = self.create_sheet(name_of_sheet=name_of_sheet, who_is=who_is)
        else:
            check = self.update_sheet(name_of_sheet=name_of_sheet, who_is=who_is)
        if check:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        elif self.result is not None:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
        else:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)

    def choose_name_of_sheet(self, name_of_sheet) -> bool | str:
        """
        Определяет, нужен ли создать новый лист или нет.

        P.S. Не читать код, пожалеете =)
        :param name_of_sheet: Название листа
        :return: Возващает bool | str ответ результата определения
        """
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        except googleapiclient.errors.HttpError as err:
            self.logger.warning(f'Проблема с соединением Google - choose_name_of_sheet {err}')
            return self.choose_name_of_sheet(name_of_sheet)
        except httplib2.error.ServerNotFoundError:
            self.logger.warning('Проблема с соединением (httplib)')
            return self.choose_name_of_sheet(name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.choose_name_of_sheet(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.choose_name_of_sheet(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.choose_name_of_sheet(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.choose_name_of_sheet(name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.choose_name_of_sheet(name_of_sheet)
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, str(sheet_id)])
        # with open('plugins/Wildberries/data/sheets.txt', 'w', encoding="UTF-8") as txt:
        #     txt.write('\n'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes))))
        os.environ[f"sheetIDs-{self.who_is}"] = ';'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes)))
        if name_of_sheet in list(map(lambda x: x[0], names_of_lists_and_codes)):
            return False
        else:
            return True

    def choose_spreadsheetId(self, who_is: str):
        """
        Записывает в self.spreadsheetId Id Таблицы, с которой надо будет работать.
        :param who_is:
        :return:
        """
        self.spreadsheetId = os.getenv(f"Wildberries-spreadsheetid-{who_is}")

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
            service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
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

    def create_sheet(self, name_of_sheet: str, who_is: str) -> bool:
        """
        Посылает запрос на сервера WildBerries, обрабатывает его, создаёт и обновляет лист под названием
        name_of_sheet с данными запроса.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return: Возвращает bool ответ результата работы всех действий (при неуспехе одного из них, возвращает False
        """
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is)
        if check:
            return False
        if self.private_create(name_of_sheet=name_of_sheet):
            return False
        if self.private_update(name_of_sheet=name_of_sheet):
            return False
        return True

    def update_sheet(self, name_of_sheet: str, who_is: str) -> bool:
        """
        Посылает запрос на сервера WildBerries, обрабатывает его, очищает и обновляет лист под названием name_of_sheet
        name_of_sheet данными с запроса.
        :param name_of_sheet: Название листа
        :param who_is: Чей токен используется
        :return: Возвращает bool ответ результата работы всех действий (при неуспехе одного из них, возвращает False
        и останавливается)
        """
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is)
        if check:
            return False
        if self.private_clear(name_of_sheet=name_of_sheet):
            return False
        if self.private_update(name_of_sheet=name_of_sheet):
            return False
        return True

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
            self.logger.warning('Проблема с соединением Google - private_create')
            return self.private_create(name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_create(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_create(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_create(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_create(name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.private_create(name_of_sheet)
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
            self.logger.warning('Проблема с соединением Google - private_clear')
            return self.private_clear(name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_clear(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_clear(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_clear(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_clear(name_of_sheet)
        except Exception as err:
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
            self.logger.warning('Проблема с соединением Google - private_update')
            return self.private_update(name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_update(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_update(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_update(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_update(name_of_sheet)
        except Exception as err:
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
        try:
            getted = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=data).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google - change_formats')
            return self.change_formats(needed_keys, name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.change_formats(needed_keys, name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.change_formats(needed_keys, name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.change_formats(needed_keys, name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.change_formats(needed_keys, name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.change_formats(needed_keys, name_of_sheet)

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
        # print('Work result')
        self.create_result()
        # with open('plugins/Wildberries/data/info_about_Result.csv', 'r') as file:
        #     csv_file = csv.reader(file, lineterminator='\r')
        #     for i in csv_file:
        #         ans.append(i)
        # try:
        #     getted = self.service.spreadsheets().values().batchGet(
        #         spreadsheetId=self.spreadsheetId,
        #         ranges="Result!A:E",
        #         valueRenderOption='FORMATTED_VALUE',
        #         dateTimeRenderOption='FORMATTED_STRING'
        #     ).execute()
        # except googleapiclient.errors.HttpError:
        #     self.logger.warning('Проблема с соединением Google - start_result1')
        #     self.LockWbResult.release()
        #     self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        #     return
        # except TimeoutError:
        #     self.logger.warning('Проблема с соединением Google (TimeoutError)')
        #     self.LockWbResult.release()
        #     self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        #     return
        design_of_result = []
        with open("plugins/Wildberries/data/info_about_Result.csv", encoding="UTF-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if '' == row:
                    continue
                else:
                    design_of_result.append(row)
        # try:
        #     values = getted['valueRanges'][0]['values']
        # except KeyError:
        #     self.LockWbResult.release()
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
        with open('plugins/Wildberries/data/sheets.txt', 'r', encoding="UTF-8") as txt:
            try:
                # check = dict(map(lambda x: x.split('='), txt.read().split('\n')))['Result']
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
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is)
        if check:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
            return
        # if new_or_not:
        # if self.private_create(name_of_sheet):
        #     check = False
        check1 = True
        if self.private_update_statements(name_of_sheet):
            check1 = False
        if check1:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        elif self.result is not None:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)
        else:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)

    def private_update_statements(self, name_of_sheet: str):
        # getted = self.service.spreadsheets().
        # get(spreadsheetId='1Hv0Pk6pRYN4bB5vJEdGnELmAPpXo0r25KatPCtCA_TE').execute()
        # getted = getted['sheets']
        # need = list()
        # for info in getted:
        #     need.append([info['properties']['title'], info['properties']['sheetId']])
        try:
            getted = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=name_of_sheet
                                                                ).execute()
        except googleapiclient.errors.HttpError:
            self.logger.warning('Проблема с соединением Google - priv_update_statements1')
            return self.private_update_statements(name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_update_statements(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_update_statements(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_update_statements(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_update_statements(name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.private_update_statements(name_of_sheet)
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
            return self.private_update_statements(name_of_sheet)
        except TimeoutError:
            self.logger.warning('Проблема с соединением Google (TimeoutError)')
            return self.private_update_statements(name_of_sheet)
        except ssl.SSLError as err:
            self.logger.warning(f'Ужасная ошибка ssl: {err}')
            return self.private_update_statements(name_of_sheet)
        except OSError as err:
            self.logger.warning(f'Вероятно TimeOutError: {err}')
            return self.private_update_statements(name_of_sheet)
        except http.client.ResponseNotReady as err:
            self.logger.warning(f'Проблема с http: {err}')
            return self.private_update_statements(name_of_sheet)
        except Exception as err:
            self.logger.error(f"Ошибка: {err}")
            return self.private_update_statements(name_of_sheet)
        return False

    def nm_report(self, who_is: str):
        check = self.start_work_with_request(self.name_of_sheet, who_is)
