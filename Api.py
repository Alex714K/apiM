import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from sheet import Sheet

import json


class Api:
    def __init__(self):
        # values = [["Ячейка B2", "Ячейка C2", "Ячейка D2"],  # Заполняем первую строку
        #                     ['25', "=6*6", "=sin(3,14/2)"]]  # Заполняем вторую строку
        self.parameters = None
        self.start()

    def start(self):
        CREDENTIALS_FILE = 'apim-415713-6b90e86bb1ba.json'
        # Читаем ключи из файла
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        # Авторизуемся в системе
        httpAuth = credentials.authorize(httplib2.Http())
        # Выбираем работу с таблицами и 4 версию API
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

        # https://docs.google.com/spreadsheets/d/1G0v5HexBJYX3moRV_0-sGTh9oVjq3FKdpZIcZr-IKmk/edit#gid=0
        # ID таблицы excel в ссылке
        spreadsheetId = '1G0v5HexBJYX3moRV_0-sGTh9oVjq3FKdpZIcZr-IKmk'
        name_of_list, new_or_not = self.parameters['dateFrom'], self.choose_name_of_list(service, spreadsheetId)
        if new_or_not:
            Sheet().create(service, spreadsheetId)
        else:
            Sheet().update(service, spreadsheetId)

    def get_parameters(self):
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))

    def choose_name_of_list(self, service: apiclient.discovery.build, spreadsheetId: str) -> bool:
        """Возвращает bool ответ, надо ли создать новый лист"""
        self.get_parameters()
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, sheet_id])
        with open('sheets.txt', 'w') as txt:
            txt.write(str(names_of_lists_and_codes))
        if self.parameters['dateFrom'] in list(map(lambda x: x[0], names_of_lists_and_codes)):
            return True
        else:
            return False
