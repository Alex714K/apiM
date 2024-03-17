import apiclient
from request_wildberries import RequestWildberries
from convert_to_list import convert_to_list

import json


class Sheet:
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    def create(self, service: apiclient.discovery.build, spreadsheetId: str):
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        dateFrom = '2024-02-29'
        json_response = RequestWildberries().start()
        values, dist = convert_to_list(json_response)
        distance = f"{self.parameters['dateFrom']}!A{1}:BI{dist}"
        results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
            "requests": [{
                    "addSheet": {
                        "properties": {
                            "title": self.parameters['dateFrom'],
                            "gridProperties": {
                                "rowCount": dist,
                                "columnCount": 30
                            }
                        }
                    }
                }]
            }).execute()
        print("\nStart updating sheet...")
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
            "valueInputOption": valueInputOption,
            "data": [
                {"range": distance,
                 "majorDimension": majorDimension,  # Сначала заполнять строки, затем столбцы
                 "values": values
                 }
            ]
        }).execute()
        print("Updating complete!")
        # print(results)

    def update(self, service: apiclient.discovery.build, spreadsheetId: str):
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        dateFrom = '2024-02-29'
        json_response = RequestWildberries().start()
        values, dist = convert_to_list(json_response)
        distance = f"{self.parameters['dateFrom']}!A{1}:BI{dist}"
        print("\nStart updating sheet...")
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
            "valueInputOption": valueInputOption,
            "data": [
                {"range": distance,
                 "majorDimension": majorDimension,  # Сначала заполнять строки, затем столбцы
                 "values": values
                 }
            ]
        }).execute()
        print("Updating complete!")
        # print(results)

    def get_parameters(self):
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
