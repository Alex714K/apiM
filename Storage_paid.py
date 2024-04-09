import apiclient
from Request_wildberries import RequestWildberries
from Converter_to_list import Converter
from Initers import Initer, Getter
import datetime
import logging


class StoragePaid(Getter, Converter):
    def __init__(self):
        super().__init__()
        self.values, self.dist, self.needed_keys = None, None, None

    def update_sheet(self, service: apiclient.discovery.build, name_of_sheet: str, dateFrom: str):
        # https://docs.google.com/spreadsheets/d/1kgPtysbiN4P46WMJcKD95ZI14SjLFeQO9-aMOCNsEbI/edit#gid=0
        spreadsheetId = '1kgPtysbiN4P46WMJcKD95ZI14SjLFeQO9-aMOCNsEbI'
        if datetime.date.today().strftime("%B") != dateFrom and datetime.date.today().day == 1:
            return
        check = self.start_work_with_request(name_of_sheet=name_of_sheet, dateFrom=dateFrom)
        if check:
            return
        dateFrom = datetime.date.today().strftime("%B")
        self.private_clear(service, spreadsheetId, name_of_sheet=dateFrom)
        self.private_update(service, spreadsheetId, name_of_sheet=dateFrom)

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
        with open('sheets.txt', 'r') as txt:
            sheets = dict(map(lambda x: x.split('='), txt.read().split('\n')))
            sheetId = sheets[name_of_sheet]
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
