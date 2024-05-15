import socket

import googleapiclient.errors
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from Wildberries.Converter_to_list import Converter
from Wildberries.Request_wildberries import RequestWildberries
import logging
import csv
from datetime import datetime


class ApiNew(Converter):
    def __init__(self):
        super().__init__()
        self.spreadsheetId = None
        self.service = None
        self.values, self.dist, self.needed_keys = None, None, None
        self.result = None

    def start(self, name_of_sheet: str, who_is: str, dateFrom: str = None, dateTo: str = None,
              date: str = None, flag=None, filterNmID: str = None, limit: str = None, from_rk: str = None,
              to_rk: str = None):
        """Запускает программу, которая записывает в таблицу excel с ID в Google Drive
        в лист 'name_of_sheet'. Данные берутся с сервера Wildberries"""
        self.choose_spreadsheetId(who_is=who_is)
        if not self.connect_to_Google():
            return
        new_or_not = self.choose_name_of_sheet(name_of_sheet=name_of_sheet)
        if new_or_not == 'error':
            return
        if new_or_not:
            check = self.create_sheet(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, dateTo=dateTo,
                                      date=date, flag=flag, filterNmID=filterNmID, limit=limit, from_rk=from_rk,
                                      to_rk=to_rk)
        else:
            check = self.update_sheet(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, dateTo=dateTo,
                                      date=date, flag=flag, filterNmID=filterNmID, limit=limit, from_rk=from_rk,
                                      to_rk=to_rk)
        if check:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet)
        else:
            self.start_work_with_list_result(name_of_sheet=name_of_sheet, bad=True)

    def choose_name_of_sheet(self, name_of_sheet) -> bool | str:
        """Возвращает bool ответ, надо ли создать новый лист. Также добавляет в sheets.txt все вкладки"""
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        except googleapiclient.errors.HttpError:
            return 'error'
        except httplib2.error.ServerNotFoundError:
            return 'error'
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, str(sheet_id)])
        with open('data/sheets.txt', 'w') as txt:
            txt.write('\n'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes))))
        if name_of_sheet in list(map(lambda x: x[0], names_of_lists_and_codes)):
            return False
        else:
            return True

    def choose_spreadsheetId(self, who_is: str):
        with open('data/spreadsheetIds.txt', 'r') as txt:
            data = txt.read().split('\n')
        data = dict(map(lambda x: x.split('='), data))
        self.spreadsheetId = data[who_is]

    def connect_to_Google(self):
        CREDENTIALS_FILE = 'Alex714K.json'
        # Читаем ключи из файла
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        try:
            # Авторизуемся в системе
            httpAuth = credentials.authorize(httplib2.Http())
            # Выбираем работу с таблицами и 4 версию API
            service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        except httplib2.error.ServerNotFoundError:
            logging.error("Google: ServerNotFound")
            print("Google: 'ServerNotFound'...\nHOW?!\n")
            return False
        except socket.gaierror:
            logging.error("gaierror")
            print("The 'gaierror' has come!\n")
            return False
        finally:
            print('Connected to Google')
        self.service = service
        return True

    def create_sheet(self, name_of_sheet: str, who_is: str, dateFrom: str,
                     dateTo: str, date: str, flag: str, filterNmID: str, limit: str, from_rk: str, to_rk: str) -> bool:
        """Создаёт список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, date=date,
                                             flag=flag, filterNmID=filterNmID, limit=limit, dateTo=dateTo,
                                             from_rk=from_rk, to_rk=to_rk)
        if check:
            return False
        self.private_create(name_of_sheet=name_of_sheet)
        self.private_update(name_of_sheet=name_of_sheet)
        return True

    def update_sheet(self, name_of_sheet: str, who_is: str, dateFrom: str,
                     dateTo: str, date: str, flag: str, filterNmID: str, limit: str, from_rk: str, to_rk: str) -> bool:
        """Очищает и обновляет список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, date=date,
                                             flag=flag, filterNmID=filterNmID, limit=limit, dateTo=dateTo,
                                             from_rk=from_rk, to_rk=to_rk)
        if check:
            return False
        if self.private_clear(name_of_sheet=name_of_sheet):
            return False
        if self.private_update(name_of_sheet=name_of_sheet):
            return False
        return True

    def start_work_with_request(self, name_of_sheet: str, who_is: str, dateFrom: str, dateTo: str, date: str, flag: str,
                                filterNmID: str, limit: str, from_rk: str, to_rk: str) -> bool:
        try:
            json_response, status_code = RequestWildberries().start(name_of_sheet=name_of_sheet, who_is=who_is,
                                                                    dateFrom=dateFrom, date=date, flag=flag,
                                                                    filterNmID=filterNmID, limit=limit, dateTo=dateTo,
                                                                    from_rk=from_rk, to_rk=to_rk)
        except TypeError:
            logging.warning(f"Нет доступа к файлу")
            print(f"Нет доступа к файлу")
            return True
        result = self.convert_to_list(json_response, name_of_sheet)
        match result:
            case 'download':
                logging.warning("Downloaded")
                print(f"Downloaded {name_of_sheet}")
                return True
            case 'is None':
                logging.warning("File = None")
                print("File = None")
                return True
            case 'is empty':
                logging.warning("File is empty")
                print("File is empty")
                return True
        self.values, self.dist, self.needed_keys = result
        return False

    def private_create(self, name_of_sheet: str) -> bool:
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
            return True
        logging.info(f"Created new sheet '{name_of_sheet}'")
        print(f"\nCreated new sheet '{name_of_sheet}'")
        return False

    def private_clear(self, name_of_sheet: str):
        if '!' in name_of_sheet:
            print(f"\nStart clearing sheet '{name_of_sheet[:name_of_sheet.index('!')]}'...")
        else:
            print(f"\nStart clearing sheet '{name_of_sheet}'...")
        try:
            getted = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=name_of_sheet
                                                                 ).execute()
        except googleapiclient.errors.HttpError:
            return True
        logging.info("Clearing complete!")
        print("Clearing complete!")
        return False

    def private_update(self, name_of_sheet: str) -> bool:
        distance = f"{name_of_sheet}"
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        print("\nStart updating sheet...")
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
            return True
        logging.info("Updating complete")
        print("Updating complete!")
        with open('data/sheets.txt', 'r') as txt:
            sheets = dict(map(lambda x: x.split('='), txt.read().split('\n')))
            sheetId = sheets[name_of_sheet]
        self.change_formats(needed_keys=self.needed_keys, sheetId=sheetId)
        return False

    def change_formats(self, needed_keys: list | None, sheetId: str):
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
            return False
        return True

    def start_work_with_list_result(self, name_of_sheet: str, bad: bool = False):
        self.create_result()
        # with open('data/info_about_Result.csv', 'r') as file:
        #     csv_file = csv.reader(file, lineterminator='\r')
        #     for i in csv_file:
        #         ans.append(i)

        getted = self.service.spreadsheets().values().batchGet(
            spreadsheetId=self.spreadsheetId,
            ranges="Result!A:E",
            valueRenderOption='FORMATTED_VALUE',
            dateTimeRenderOption='FORMATTED_STRING'
        ).execute()

        values = getted['valueRanges'][0]['values']
        # очистка от лишних пустых элементов списка (а они бывают)
        for i in range(len(values)):
            if '' in values[i]:
                values[i] = values[i][:values[i].index('')]

        ind = (list(map(lambda x: x[0], values))).index(name_of_sheet)
        if bad:
            if len(values[ind]) > 3:
                values[ind][3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                values[ind][4] = f"Ошибка: {self.result}"
            else:
                values[ind].extend(
                    [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Успешно записано строк: {self.dist}"])
        else:
            if len(values[ind]) > 3:
                values[ind][3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                values[ind][4] = f"Успешно записано строк: {self.dist}"
            else:
                values[ind].extend([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Успешно записано строк: {self.dist}"])

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
            return

    def create_result(self):
        with open('data/sheets.txt', 'r') as txt:
            try:
                check = dict(map(lambda x: x.split('='), txt.read().split('\n')))['Result']
            except KeyError:
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
                values = list()
                with open('data/info_about_Result.csv', 'r') as file:
                    csv_file = csv.reader(file)
                    for i in csv_file:
                        if '' == i:
                            continue
                        else:
                            values.append(i)
                getted = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": "Result!A:E",
                         "majorDimension": "ROWS",
                         "values": values
                         }
                    ]
                }).execute()
