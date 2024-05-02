import socket
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from Converter_to_list import Converter
from Wildberries.Request_wildberries import RequestWildberries
from Initers import Getter
import logging
from Storage_paid import StoragePaid
from Statements import Statements


class ApiNew(Converter):
    def __init__(self):
        super().__init__()
        self.spreadsheetId = None
        self.service = None
        self.values, self.dist, self.needed_keys = None, None, None

    def start(self, name_of_sheet: str, who_is: str, dateFrom: str = None, dateTo: str = None,
              date: str = None, flag=None, filterNmID: str = None, limit: str = None, from_rk: str = None,
              to_rk: str = None):
        """Запускает программу, которая записывает в таблицу excel с ID в Google Drive
        в лист 'name_of_sheet'. Данные берутся с сервера Wildberries"""
        self.choose_spreadsheetId(who_is=who_is)
        if self.connect_to_Google():
            return
        new_or_not = self.choose_name_of_sheet(name_of_sheet=name_of_sheet)
        if new_or_not:
            self.create_sheet(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, dateTo=dateTo, date=date,
                              flag=flag, filterNmID=filterNmID, limit=limit, from_rk=from_rk, to_rk=to_rk)
        else:
            self.update_sheet(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, dateTo=dateTo, date=date,
                              flag=flag, filterNmID=filterNmID, limit=limit, from_rk=from_rk, to_rk=to_rk)

    def choose_name_of_sheet(self, name_of_sheet) -> bool:
        """Возвращает bool ответ, надо ли создать новый лист"""
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
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
            return True
        except socket.gaierror:
            logging.error("gaierror")
            print("The 'gaierror' has come!\n")
            return True
        finally:
            print('Connected to Google')
        self.service = service
        return False

    def create_sheet(self, name_of_sheet: str, who_is: str, dateFrom: str,
                     dateTo: str, date: str, flag: str, filterNmID: str, limit: str, from_rk: str, to_rk: str):
        """Создаёт список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, date=date, flag=flag,
                                             filterNmID=filterNmID, limit=limit, dateTo=dateTo, from_rk=from_rk,
                                             to_rk=to_rk)
        if check:
            return
        self.private_create(name_of_sheet=name_of_sheet)
        self.private_update(name_of_sheet=name_of_sheet)

    def update_sheet(self, name_of_sheet: str, who_is: str, dateFrom: str,
                     dateTo: str, date: str, flag: str, filterNmID: str, limit: str, from_rk: str, to_rk: str):
        """Очищает и обновляет список под названием 'name_of_sheet' с данными из сервера Wildberries"""
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, who_is=who_is, dateFrom=dateFrom, date=date, flag=flag,
                                             filterNmID=filterNmID, limit=limit, dateTo=dateTo, from_rk=from_rk,
                                             to_rk=to_rk)
        if check:
            return
        self.private_clear(name_of_sheet=name_of_sheet)
        self.private_update(name_of_sheet=name_of_sheet)
        # print(results)

    def start_work_with_request(self, name_of_sheet: str, who_is: str, dateFrom: str, dateTo: str, date: str, flag: str,
                                filterNmID: str, limit: str, from_rk: str, to_rk: str) -> bool:
        try:
            json_response, status_code = RequestWildberries().start(name_of_sheet=name_of_sheet, who_is=who_is,
                                                                    dateFrom=dateFrom, date=date, flag=flag,
                                                                    filterNmID=filterNmID, limit=limit, dateTo=dateTo,
                                                                    from_rk=from_rk, to_rk=to_rk)
        except TypeError:
            logging.warning(f"Нет доступа к файлу '{name_of_sheet}' на сервере")
            print(f"Нет доступа к файлу '{name_of_sheet}' на сервере")
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

    def private_create(self, name_of_sheet: str):
        columnCount = len(self.values[0])  # кол-во столбцов
        name_of_sheet = name_of_sheet
        results = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body={
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
        logging.info(f"Created new sheet '{name_of_sheet}'")
        print(f"\nCreated new sheet '{name_of_sheet}'")

    def private_clear(self, name_of_sheet: str):
        print(f"\nStart clearing sheet '{name_of_sheet}'...")
        results = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=name_of_sheet
                                                             ).execute()
        # with open('sheets.txt', 'r') as txt:
        #     sheets = dict(map(lambda x: x.split('='), txt.read().split('\n')))
        #     sheetId = sheets[name_of_sheet]
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
        logging.info("Clearing complete!")
        print("Clearing complete!")

    def private_update(self, name_of_sheet: str):
        distance = f"{name_of_sheet}"
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        print("\nStart updating sheet...")
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
            "valueInputOption": valueInputOption,
            "data": [
                {"range": distance,
                 "majorDimension": majorDimension,
                 "values": self.values
                 }
            ]
        }).execute()
        logging.info("Updating complete")
        print("Updating complete!")
        with open('sheets.txt', 'r') as txt:
            sheets = dict(map(lambda x: x.split('='), txt.read().split('\n')))
            sheetId = sheets[name_of_sheet]
        self.change_formats(needed_keys=self.needed_keys, sheetId=sheetId)

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
        results = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=data).execute()
