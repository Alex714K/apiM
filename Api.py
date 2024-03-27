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
        self.get_parameters()

    def start(self, name_of_sheet: str, dateFrom: str = None, date: str = None, flag: str = None, filterNmID='',
              limit: str = None, dateTo: str = None, from_rk: str = None, to_rk: str = None):
        """Запускает программу, которая записывает в таблицу excel с ID в Google Drive
        в лист 'name_of_sheet'. Данные берутся с сервера Wildberries"""
        CREDENTIALS_FILE = 'Alex714K.json'
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
        name_of_list = self.parameters['dateFrom']
        new_or_not = self.choose_name_of_sheet(service, spreadsheetId, name_of_sheet=name_of_sheet)
        if new_or_not:
            Sheet().create(service, spreadsheetId, name_of_sheet=name_of_sheet, dateFrom=dateFrom, date=date, flag=flag,
                           limit=limit, dateTo=dateTo, from_rk=from_rk, to_rk=to_rk)
        else:
            Sheet().update(service, spreadsheetId, name_of_sheet=name_of_sheet, dateFrom=dateFrom, date=date, flag=flag,
                           limit=limit, dateTo=dateTo, from_rk=from_rk, to_rk=to_rk)

    def get_parameters(self):
        """Достаёт словарь параметров в parameters.txt"""
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))

    @staticmethod
    def choose_name_of_sheet(service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet) -> bool:
        """Возвращает bool ответ, надо ли создать новый лист"""
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, str(sheet_id)])
        with open('sheets.txt', 'w') as txt:
            txt.write('\n'.join(list(map(lambda x: '='.join(x), names_of_lists_and_codes))))
        if name_of_sheet in list(map(lambda x: x[0], names_of_lists_and_codes)):
            return False
        else:
            return True
