import apiclient
from request_wildberries import RequestWildberries
from convert_to_list import convert_to_list
import json
import numpy


class Sheet:
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    @staticmethod
    def create(service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str, dateFrom: str, date: str,
               flag: str):
        """Создаёт список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        json_response = RequestWildberries().start(name_of_sheet=name_of_sheet, dateFrom=dateFrom, date=date, flag=flag)
        values, dist = convert_to_list(json_response)
        columnCount = len(values[0])  # кол-во столбцов
        name_of_sheet = name_of_sheet
        results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
            "requests": [{
                    "addSheet": {
                        "properties": {
                            "title": name_of_sheet,
                            "gridProperties": {
                                "rowCount": dist,
                                "columnCount": columnCount
                            }
                        }
                    }
                }]
            }).execute()
        print(f"\nCreated new sheet '{name_of_sheet}'")
        print("\nStart updating sheet...")
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        distance = f"{name_of_sheet}!A{1}:BI{dist}"
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
        # print(results)

    @staticmethod
    def update(service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str, dateFrom: str, date: str,
               flag: str):
        """Очищает и обновляет список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        json_response = RequestWildberries().start(name_of_sheet=name_of_sheet, dateFrom=dateFrom, date=date, flag=flag)
        values, dist = convert_to_list(json_response)
        distance = f"{name_of_sheet}!A{1}:BI{dist}"
        print("\nStart clearing sheet...")
        results = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range=name_of_sheet
                                                        ).execute()
        print("Clearing complete!")
        print("\nStart updating sheet...")
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
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
        # print(results)

    def get_parameters(self):
        """Достаёт словарь параметров в parameters.txt"""
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
