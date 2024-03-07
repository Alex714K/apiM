import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import request_wildberries
import convert_to_list


def start():
    CREDENTIALS_FILE = 'apim-415713-6b90e86bb1ba.json'
    json_response = request_wildberries.start()
    values, dist = convert_to_list.start(json_response)
    # values = [["Ячейка B2", "Ячейка C2", "Ячейка D2"],  # Заполняем первую строку
    #                     ['25', "=6*6", "=sin(3,14/2)"]]  # Заполняем вторую строку
    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])

    # Авторизуемся в системе
    httpAuth = credentials.authorize(httplib2.Http())
    # Выбираем работу с таблицами и 4 версию API
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # https://docs.google.com/spreadsheets/d/1G0v5HexBJYX3moRV_0-sGTh9oVjq3FKdpZIcZr-IKmk/edit#gid=0
    spreadsheetId = '1G0v5HexBJYX3moRV_0-sGTh9oVjq3FKdpZIcZr-IKmk'

    valueInputOption = "USER_ENTERED"  # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    # majorDimension = "COLUMNS"  # список - столбец (не работает)
    majorDimension = "ROWS"  # список - строка
    times = dist % 1000+1
    distance = f"Лист1!A{1}:N{dist}"
    print("Start updating sheet...")
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
    print(results)
