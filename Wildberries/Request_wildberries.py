import logging
import sys
import uuid
import requests
import datetime
import json
import socket
from Initers import Getter


class RequestWildberries(Getter):
    def __init__(self):
        super().__init__()
        self.name_of_sheet = None

    def start(self, name_of_sheet: str, who_is: str, storage_paid=False, statements=False):
        """Формирует с отправляет запрос на сервера Wildberries для получения различных данных (в зависимости от
        вводимых параветров). При успешном получении возвращает json-объект. При ошибке ничего не возвращает и
        пишет ошибку в консоль"""
        self.name_of_sheet = name_of_sheet
        match name_of_sheet:
            case 'nm_report':
                return self.nm_report(who_is)
        # Ссылка
        try:
            url = self.parameters[f"url_{name_of_sheet}"]
        except KeyError:
            print("Wrong name of sheet")
            logging.critical("Wrong name of sheet!")
            sys.exit("Wrong name of sheet!")
        # Токен
        with open('Wildberries/data/tokens.txt') as txt:
            tokens = dict(map(lambda x: x.split('='), txt.read().split('\n')))
        authorization = tokens[who_is]
        headers = {
            'Authorization': authorization
        }
        # Выполняем запрос
        try:
            # Если только через ссылку
            if name_of_sheet in ['stocks', 'orders_1mnth', 'orders_1week', 'orders_2days', 'orders_today',
                                 'tariffs_boxes', 'tariffs_pallet', 'statements', 'prices', 'rk']:
                params = self.make_params()
                url_for_reqst = self.make_request(url, params)
                response = requests.get(url_for_reqst, headers=headers)
            # Если через json
            elif name_of_sheet in []:
                params = self.make_params()
                response = requests.get(url, headers=headers, json=params)
            else:
                sys.exit('Man, you forget smth in Request_wildberries.py')
        except socket.gaierror:
            logging.error(f"gaierror ({self.name_of_sheet})")
            print(f"The 'gaierror' has come ({self.name_of_sheet})!\n")
            return 'Проблема с соединением'
        if not response:
            logging.warning(f"Ошибка выполнения запроса:\nHttp статус: {response.status_code} ( {response.reason} )")
            print("Ошибка выполнения запроса:")
            print(url)
            print(f"Http статус: {response.status_code} ( {response.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return response.status_code, response.reason
        else:
            try:
                # Преобразуем ответ в json-объект
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                print(f'Missing json file in {self.name_of_sheet}')
                return 'Missing json file'
            # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response, d, ensure_ascii=False, indent=4)
            logging.info(f"Http статус: {response.status_code}, name_of_sheet: {self.name_of_sheet}")
            print("Успешно")
            print(url)
            print(f"Http статус: {response.status_code}")
            return json_response, response.status_code

    @staticmethod
    def make_request(url, kwargs: dict) -> str:
        """Формируей ссылку для отправки запроса на сервер Wildberries"""
        if kwargs == {}:
            fin_url = f"{url}"
        else:
            fin_url = f"{url}?"
            a = True
            for key, item in kwargs.items():
                if a:
                    if item != None:
                        if 'rk' in key:
                            fin_url += f"{key[:-3]}={item}"
                        else:
                            fin_url += f"{key}={item}"
                        a = False
                else:
                    if item != None:
                        if 'rk' in key:
                            fin_url += f"&{key[:-3]}={item}"
                        else:
                            fin_url += f"&{key}={item}"

        return fin_url

    @staticmethod
    def choose_dates_old(dateFrom: str = None, date: str = None, dateTo: str = None) -> tuple[str, str, str]:
        """Если вводиться не дата, а слова: today, 2days, 1week, 1mnth; то выводятся сегодняшняя дата и до -30 дней"""
        match dateFrom:
            case 'today':
                dateFrom = datetime.date.today()
            case '2days':
                dateFrom = datetime.date.today() - datetime.timedelta(days=2)
            case '1week':
                dateFrom = datetime.date.today() - datetime.timedelta(weeks=1)
            case '1mnth':
                dateFrom = datetime.date.today() - datetime.timedelta(days=30)
            case 'statements':
                first_day = datetime.date.today().weekday() + 7
                last_day = first_day - 6
                dateFrom = datetime.date.today() - datetime.timedelta(days=first_day)
                dateTo = datetime.date.today() - datetime.timedelta(days=last_day)
            case 'storage_paid':
                year = datetime.date.today().year
                month = (datetime.date.today() - datetime.timedelta(days=30)).month
                last_day = (datetime.date.today() - datetime.timedelta(days=1)).day
                dateFrom = datetime.date(year, month, 1).strftime("%Y-%m-%d")
                dateTo = datetime.date(year, month, last_day).strftime("%Y-%m-%d")

        match date:
            case 'today':
                date = datetime.date.today()
            case '2days':
                date = datetime.date.today() - datetime.timedelta(days=2)
            case '1week':
                date = datetime.date.today() - datetime.timedelta(weeks=1)
            case '1mnth':
                date = datetime.date.today() - datetime.timedelta(days=30)
            case 'tariffs':
                with open('Wildberries/data/date_of_tariffs.txt', 'r') as txt:
                    date = txt.read()

        match dateTo:
            case 'today':
                dateTo = datetime.date.today()
            case '2days':
                dateTo = datetime.date.today() - datetime.timedelta(days=2)
            case '1week':
                dateTo = datetime.date.today() - datetime.timedelta(weeks=1)
            case '1mnth':
                dateTo = datetime.date.today() - datetime.timedelta(days=30)
        return dateFrom, date, dateTo

    def make_params(self) -> dict | dict[str, int] | dict[str, str]:
        match self.name_of_sheet:
            case 'stocks':
                params = {'dateFrom': '2024-03-25'}
            case 'orders_today':
                params = {
                    'dateFrom': datetime.date.today().strftime("%Y-%m-%d"),
                    'flag': 1
                }
            case 'orders_2days':
                params = {'dateFrom': (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")}
            case 'orders_1week':
                params = {'dateFrom': (datetime.date.today() - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")}
            case 'orders_1mnth':
                params = {'dateFrom': (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")}
            case 'tariffs_boxes':
                params = {'date': open('Wildberries/data/date_of_tariffs.txt', 'r').read()}
            case 'tariffs_pallet':
                params = {'date': open('Wildberries/data/date_of_tariffs.txt', 'r').read()}
            case 'prices':
                params = {'limit': 1000}
            case 'fixed_prices':
                params = {'limit': 1000}
            case 'rk':
                params = {
                    'from_rk': '2024-02-01',
                    'to_rk': '2024-02-29'
                }
            case 'statements':
                first_day = datetime.date.today().weekday() + 7
                last_day = first_day - 6
                params = {
                    'dateFrom': (datetime.date.today() - datetime.timedelta(days=first_day)).strftime("%Y-%m-%d"),
                    'dateTo': (datetime.date.today() - datetime.timedelta(days=last_day)).strftime("%Y-%m-%d")
                }
            case _:
                params = {}
        return params

    def nm_report(self, who_is):
        url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads'
        iduu = str(uuid.uuid4())
        # Токен
        with open('Wildberries/data/tokens.txt') as txt:
            tokens = dict(map(lambda x: x.split('='), txt.read().split('\n')))
        authorization = tokens[who_is]
        headers = {
            'Authorization': authorization
        }
        # Параметры
        params = {
            'id': iduu,
            'reportType': 'DETAIL_HISTORY_REPORT',
            'params': {
                'startDate': (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                'endDate': (datetime.date.today()).strftime('%Y-%m-%d')
            }
        }
        response = requests.post(url, headers=headers, json=params)
        flag = True
        while flag:
            if datetime.datetime.today().second % 15 == 0:
                response = requests.get(url, headers=headers)
                json_response = response.json()
                if json_response["data"] is None:
                    print(json_response)
                    break
                for element in json_response["data"]:
                    if element['id'] == iduu and element['status'] == "SUCCESS":
                        flag = False
        if flag:
            return None, None
        response = requests.get(url, headers=headers)
        return list(map(lambda x: x.split(';'), response.content.decode("utf-8")))
