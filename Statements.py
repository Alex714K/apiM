import apiclient
from Request_wildberries import RequestWildberries
from Converter_to_list import Converter
from Initers import Getter
import datetime
import logging


class Statements(Getter, Converter):
    def __init__(self, spreadsheetId):
        super().__init__()
        # https://docs.google.com/spreadsheets/d/1Hv0Pk6pRYN4bB5vJEdGnELmAPpXo0r25KatPCtCA_TE/edit#gid=0
        self.spreadsheetId = '1Hv0Pk6pRYN4bB5vJEdGnELmAPpXo0r25KatPCtCA_TE'
        self.values, self.dist, self.needed_keys = None, None, None
        self.name_of_sheet = (datetime.date.today() - datetime.timedelta(weeks=1)).isocalendar()[1]

    def start_work_with_request(self, name_of_sheet: str, dateFrom: str) -> bool:
        try:
            json_response, status_code = RequestWildberries().start(name_of_sheet=name_of_sheet, dateFrom=dateFrom,
                                                                    storage_paid=True)
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

    def create_sheet(self, service: apiclient.discovery.build, name_of_sheet_for_request: str, dateFrom: str):
        check = self.start_work_with_request(name_of_sheet=name_of_sheet_for_request, dateFrom=dateFrom)
        if check:
            return
        self.private_create(service, self.spreadsheetId, name_of_sheet=self.name_of_sheet)
        self.private_update(service, self.spreadsheetId, name_of_sheet=self.name_of_sheet)

    def update_sheet(self, service: apiclient.discovery.build, name_of_sheet: str, dateFrom: str):
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, dateFrom=dateFrom)
        if check:
            return
        self.private_clear(service, self.spreadsheetId, name_of_sheet=self.name_of_sheet)
        self.private_update(service, self.spreadsheetId, name_of_sheet=self.name_of_sheet)

    def private_create(self, service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str):
        columnCount = len(self.values[0])  # кол-во столбцов
        results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
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

    @staticmethod
    def private_clear(service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str):
        print(f"\nStart clearing sheet '{name_of_sheet}'...")
        results = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range=name_of_sheet
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

    def private_update(self, service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str):
        distance = f"{name_of_sheet}"
        valueInputOption = "USER_ENTERED"
        majorDimension = "ROWS"  # список - строка
        print("\nStart updating sheet...")
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
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
        sheetId = self.get_sheet_id(service, spreadsheetId, name_of_sheet)
        self.change_formats(service, spreadsheetId, needed_keys=self.needed_keys, sheetId=sheetId)

    @staticmethod
    def change_formats(service: apiclient.discovery.build, spreadsheetId: str, needed_keys: list | None, sheetId: str):
        if needed_keys is None:
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
        results = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=data).execute()

    @staticmethod
    def get_sheet_id(service: apiclient.discovery.build, spreadsheetId: str, name_of_sheet: str) -> str:
        needed_sheet_id = None
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
        names_of_lists_and_codes = list()
        sheets = sheet_metadata.get('sheets', '')
        for one_sheet in sheets:
            title = one_sheet.get("properties", {}).get("title", "Sheet1")
            sheet_id = one_sheet.get("properties", {}).get("sheetId", 0)
            names_of_lists_and_codes.append([title, str(sheet_id)])
            if name_of_sheet == title:
                needed_sheet_id = sheet_id
        return needed_sheet_id
