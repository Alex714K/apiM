import sys

import requests
import json


class RequestWildberries:
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    def start(self) -> list:
        with open('wildberries_token.txt', 'r') as txt:
            authorization = txt.read()
        # Дата
        dateFrom = '2024-02-29'
        dateFrom = self.parameters['dateFrom']
        date_to = '2024-03-03'
        flag = '1'
        flag = self.parameters['flag']
        # Ссылка
        url = 'https://statistics-api.wildberries.ru/api/v1/supplier/sales'
        url = self.parameters['url']
        # Ссылка запроса
        request = f"{url}?dateFrom={dateFrom}&flag={flag}"
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
            with open('data.json') as data:
                return json.load(data)
            # sys.exit(1)
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

    def get_parameters(self):
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
