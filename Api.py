import socket
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from Initers import Initer
import logging
from Storage_paid import StoragePaid
from Statements import Statements
from Wildberries.ApiWB import ApiNew
from datetime import datetime


class Api(Initer):
    def start(self, name_of_sheet: str, who_is: str, folder: str, dateFrom: str = None, date: str = None,
              flag: str = None, filterNmID=None, limit: str = None, dateTo: str = None, from_rk: str = None,
              to_rk: str = None):
        """Основной старт. От него зависит, что запуститься. Ничего не возвращает."""
        print('-------------------------------------------------------------------------------------------------------')
        print(datetime.now().strftime(""))
        logging.info(f"Started '{name_of_sheet}'")
        match folder:
            case 'WB':
                ApiNew().start(name_of_sheet, who_is, dateFrom=dateFrom, dateTo=dateTo, date=date, flag=flag,
                               filterNmID=filterNmID, limit=limit, from_rk=from_rk, to_rk=to_rk)

    @staticmethod
    def choose_name_of_sheet(service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet) -> bool:
        """Возвращает bool ответ, надо ли создать новый лист. Также добавляет в sheets.txt все вкладки"""
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

    def connect_to_Google(self):  # Need to move into place, where I work with sheet
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
            return
        except socket.gaierror:
            logging.error("gaierror")
            print("The 'gaierror' has come!\n")
            return
        finally:
            print('Connected to Google')
