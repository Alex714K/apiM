import sys

import requests
import json

import pickle
import os

import convert_to_list


def start():
    with open('wildberries_token.txt', 'r') as txt:
        authorization = txt.read()
    # Дата
    date = '2019-06-20'
    # Ссылка
    url = 'https://statistics-api.wildberries.ru/api/v1/supplier/incomes'
    # Ссылка запроса
    request = f"{url}?dateFrom={date}"
    # Токен
    headers = {
        'Authorization': authorization
    }

    # Выполняем запрос
    response = requests.get(request, headers=headers)
    if not response:
        print("Ошибка выполнения запроса:")
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        with open('data.json', 'r') as file:
            return file.read()
    else:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # print(json.dumps(json_response, ensure_ascii=False, indent=4))
        # Записываем данные в файл
        with open('data.json', 'w') as d:
            json.dump(json_response, d)
        print("Успешно")
        print(request)
        print('Http статус:', response.status_code)
        return json_response
