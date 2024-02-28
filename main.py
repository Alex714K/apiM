import sys

import requests
import json

import pickle
import os


# Дата
date = '2019-06-20'
# Ссылка
url = 'https://statistics-api.wildberries.ru/api/v1/supplier/incomes'
# Ссылка запроса
request = f"{url}?dateFrom={date}"
# Токен
headers = {
    'Authorization': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMjI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyMTk1NzQwN'
                     'iwiaWQiOiJiNjNiOGE2MC04N2U4LTRlMDQtYTQ0NS0xY2VlMDMwMTA3MGQiLCJpaWQiOjEyMjk3NDMxLCJvaWQiOjYxMzE4L'
                     'CJzIjoxMDczNzQxODYwLCJzaWQiOiIwZjI0ZDVhMC1mYjQ5LTU0ZDctOTQ2MS1lN2JhNDNhYmMxYTAiLCJ0IjpmYWxzZSwid'
                     'WlkIjoxMjI5NzQzMX0.m5Fopqp00mOsrN4dveNoxSJzxe7SnNKJQsEaH8chauoZbdTP3mvOko6s7VCK8hDi36vjuJjPdxMtb'
                     'X-UVqMbMA'
}

# Выполняем запрос
response = requests.get(request, headers=headers)
if not response:
    print("Ошибка выполнения запроса:")
    print(request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
else:
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Записываем данные в файл
    with open('data.json', 'w') as d:
        json.dump(json_response, d)
    print("Успешно")
    print(request)
    print('Http статус:', response.status_code)