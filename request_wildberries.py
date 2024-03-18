import sys

import requests
import json


class RequestWildberries:
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    def start(self, name_of_sheet: str) -> list:
        with open('wildberries_token.txt', 'r') as txt:
            authorization = txt.read()
        # Дата
        dateFrom = self.parameters['dateFrom']
        # Флажок
        flag = self.parameters['flag']
        # Ссылка
        url = self.parameters[f"url_{name_of_sheet}"]
        # Ссылка запроса
        request = f"{url}?dateFrom={dateFrom}&flag={flag}"
        # request = self.make_request(url, dateFrom, flag)
        # Токен
        headers = {
            'Authorization': authorization
        }

        # Выполняем запрос
        response = requests.get(request, headers=headers)
        if not response:
            print("Ошибка выполнения запроса:")
            print(request)
            print(f"Http статус: {response.status_code} ( {response.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            sys.exit(1)
        else:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл
            with open('data.json', 'w') as d:
                json.dump(json_response, d)
            print("Успешно")
            print(request)
            print(f'Http статус: {response.status_code}')
            return json_response

    def make_request(self, url,  *args) -> str:
        pass

    def get_parameters(self):
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
