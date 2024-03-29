import apiclient
from request_wildberries import RequestWildberries
from convert_to_list import convert_to_list
import json
import numpy


class Sheet:
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    def create(self, service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str, dateFrom: str, date: str,
               flag: str, limit: str, dateTo: str, from_rk: str, to_rk: str):
        """Создаёт список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        try:
            json_response, status_code = RequestWildberries().start(name_of_sheet=name_of_sheet, dateFrom=dateFrom,
                                                                    date=date, flag=flag, limit=limit, dateTo=dateTo,
                                                                    from_rk=from_rk, to_rk=to_rk)
        except TypeError:
            print(f"Нет доступа к файлу '{name_of_sheet}' на сервере")
            return
        try:
            values, dist, needed_keys = convert_to_list(json_response, name_of_sheet)
        except TypeError:
            print('Файл скачен на устройство')
            return
        columnCount = len(values[0])  # кол-во столбцов
        name_of_sheet = name_of_sheet
        results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
            "requests": [{
                "addSheet": {
                    "properties": {
                        "title": name_of_sheet,
                        "gridProperties": {
                            "rowCount": dist + 100,
                            "columnCount": columnCount + 5
                        }
                    }
                }
            }]
        }).execute()
        print(f"\nCreated new sheet '{name_of_sheet}'")
        print("\nStart updating sheet...")
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        valueInputOption = "USER_ENTERED"
        valueInputOption = "RAW"
        majorDimension = "ROWS"  # список - строка
        distance = f"{name_of_sheet}"
        with open('sheets.txt', 'r') as txt:
            sheets = dict(map(lambda x: x.split('='), txt.read().split('\n')))
            sheetId = sheets[name_of_sheet]
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
            "valueInputOption": valueInputOption,
            "data": [
                {"range": distance,
                 "majorDimension": majorDimension,
                 "values": values
                 }
            ]
        }).execute()
        print("Updating complete!\n")
        self.change_formats(service, spreadsheetId, needed_keys=needed_keys, sheetId=sheetId)
        # print(results)

    def update(self, service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str, dateFrom: str, date: str,
               flag: str, limit: str, dateTo: str, from_rk: str, to_rk: str):
        """Очищает и обновляет список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        try:
            json_response, status_code = RequestWildberries().start(name_of_sheet=name_of_sheet, dateFrom=dateFrom,
                                                                    date=date, flag=flag, limit=limit, dateTo=dateTo,
                                                                    from_rk=from_rk, to_rk=to_rk)
        except TypeError:
            print(f"There is no access to the file '{name_of_sheet}' on the server of Wildberries\n")
            return
        try:
            values, dist, needed_keys = convert_to_list(json_response, name_of_sheet)
        except TypeError:
            print(f"The file '{name_of_sheet}' has been downloaded to the device")
            return
        distance = f"{name_of_sheet}"
        valueInputOption = "USER_ENTERED"
        valueInputOption = "RAW"
        majorDimension = "ROWS"  # список - строка
        responseValueRenderOption = 'UNFORMATTED_VALUE'
        with open('sheets.txt', 'r') as txt:
            sheets = dict(map(lambda x: x.split('='), txt.read().split('\n')))
            sheetId = sheets[name_of_sheet]
        print(f"\nStart clearing sheet '{name_of_sheet}'...")
        results = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range=name_of_sheet
                                                        ).execute()
        # results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
        #     "requests": [
        #         {
        #          "updateCells": {
        #              "range": {"sheetId": sheetId},
        #              "fields": "*"
        #              }
        #          }
        #     ]
        # }).execute()
        print("Clearing complete!")
        print("\nStart updating sheet...")
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
            "valueInputOption": valueInputOption,
            "data": [
                {"range": distance,
                 "majorDimension": majorDimension,
                 "values": values
                 }
            ]
        }).execute()
        print("Updating complete!\n")
        self.change_formats(service, spreadsheetId, needed_keys=needed_keys, sheetId=sheetId)
        # print(results)

    @staticmethod
    def change_formats(service: apiclient.discovery.build, spreadsheetId: str, needed_keys, sheetId):
        results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheetId,
                            "startColumnIndex": needed_keys[0],
                            "endColumnIndex": needed_keys[0] + 1
                        },
                        "cell": {
                            "userEnteredValue": {"stringValue": "1000"},
                            "formattedValue": "1000",
                            "userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "0,00"}}
                        },
                        "fields": "userEnteredFormat(numberFormat)"
                    }
                }
            ]
        }).execute()

    def get_parameters(self):
        """Достаёт словарь параметров в parameters.txt"""
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
