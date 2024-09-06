import sys
import time
from threading import RLock
import uuid
import requests
import datetime
import socket
from logging import getLogger
import os


class RequestWildberries:
    def __init__(self, LockWbRequest: RLock):
        self.name_of_sheet = None
        self.LockWbRequest = LockWbRequest
        self.logger = getLogger("RequestWildberries")

    def start(self, name_of_sheet: str, who_is: str):
        match name_of_sheet:
            case "stocks_hard":
                return self.stocks_hard(who_is)
            case "nm_report":
                return self.nm_report(who_is)
            case _:
                return self.simple_start(name_of_sheet, who_is)

    def simple_start(self, name_of_sheet: str, who_is: str, storage_paid=False, statements=False):
        """Формирует с отправляет запрос на сервера Wildberries для получения различных данных (в зависимости от
        вводимых параветров). При успешном получении возвращает json-объект. При ошибке ничего не возвращает и
        пишет ошибку в консоль"""
        self.name_of_sheet = name_of_sheet

        # Ссылка
        url = os.getenv(f"Wildberries-url-{name_of_sheet}")
        if url == None:
            self.logger.critical(f"Man, you forget {name_of_sheet} in Request_wildberries.py")
            sys.exit(f"Man, you forget {name_of_sheet} in Request_wildberries.py")

        # Токен
        headers = {
            "Authorization": os.getenv(f"Wildberries-token-{who_is}")
        }

        # Выполняем запрос
        try:
            # Если только через ссылку
            if name_of_sheet in ["stocks", "orders_1mnth", "orders_1week", "orders_2days", "orders_today",
                                 "tariffs_boxes", "tariffs_pallet", "statements", "prices", "fixed_prices", "rk",
                                 "stat_prodvigene"]:
                params = self.make_params()
                url_for_reqst = self.make_request(url, params)
                response = requests.get(url_for_reqst, headers=headers)
            # Если через json и ссылку
            elif name_of_sheet in []:
                params = self.make_params()
                response = requests.get(url, headers=headers, json=params)
            else:
                self.logger.critical(f"Man, you forget {name_of_sheet} in Request_wildberries.py")
                sys.exit(f"Man, you forget {name_of_sheet} in Request_wildberries.py")
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({self.name_of_sheet})")
            return "Проблема с соединением"

        if not response:
            self.logger.warning(f"{name_of_sheet} - Http статус: {response.status_code} ( {response.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return response.status_code, response.reason
        else:
            try:
                # Преобразуем ответ в json-объект
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {self.name_of_sheet}")
                return "Missing json file"
            # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response, d, ensure_ascii=False, indent=4)
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {self.name_of_sheet}")
            return json_response, response.status_code

    def stocks_hard(self, who_is: str):
        self.name_of_sheet = "stocks_hard"
        # Токен
        headers = {
            "Authorization": os.getenv(f"Wildberries-token-{who_is}")
        }
        params = {
            "groupByBrand": "true",
            "groupBySubject": "true",
            "groupBySa": "true",
            "groupByNm": "true",
            "groupByBarcode": "true",
            "groupBySize": "true"
        }
        url = "https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains"
        url = self.make_request(url, params)
        try:
            response = requests.get(url, headers=headers)
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({self.name_of_sheet})")
            return "Проблема с соединением"
        try:
            task_id = response.json()["data"]["taskId"]
        except KeyError:
            self.logger.debug(f"stocks_hard - code:{response.status_code}, reason:{response.reason}")
            time.sleep(60)
            return self.stocks_hard(who_is)
        url = f"https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/status"
        while True:
            try:
                response = requests.get(url, headers=headers)
            except socket.gaierror:
                self.logger.warning(f"gaierror with Google ({self.name_of_sheet})")
                time.sleep(5)
                continue
            json_response = response.json()
            if json_response["data"]["status"] == "done":
                break
            else:
                self.logger.debug(f"stocks_hard - status:{json_response["data"]["status"]}")
                time.sleep(4)
        url = f"https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/download"
        response = requests.get(url, headers=headers)

        if not response:
            self.logger.warning(f"stocks_hard - Http статус: {response.status_code} ( {response.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return response.status_code, response.reason
        else:
            try:
                # Преобразуем ответ в json-объект
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {self.name_of_sheet}")
                return "Missing json file"
            # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response, d, ensure_ascii=False, indent=4)
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {self.name_of_sheet}")
            return {"json": json_response, "warehouses": self.get_warehouses(who_is)}, response.status_code

    def get_warehouses(self, who_is: str):
        url = "https://supplies-api.wildberries.ru/api/v1/warehouses"
        # Токен
        headers = {
            "Authorization": os.getenv(f"Wildberries-token-{who_is}")
        }
        try:
            response = requests.get(url, headers=headers)
        except socket.gaierror:
            time.sleep(10)
            return self.get_warehouses(who_is)
        return list(map(lambda x: x["name"].replace("(", "").replace(")", ""), response.json()))

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
                with open('plugins/Wildberries/data/date_of_tariffs.txt', 'r') as txt:
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
                params = {'date': open('plugins/Wildberries/data/date_of_tariffs.txt', 'r').read()}
            case 'tariffs_pallet':
                params = {'date': open('plugins/Wildberries/data/date_of_tariffs.txt', 'r').read()}
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
            case "stat_prodvigene":
                params = {}
            case _:
                params = {}
        return params

    def nm_report(self, who_is):
        url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads'
        iduu = str(uuid.uuid4())
        headers = {
            "Authorization": os.getenv(f"Wildberries-token-{who_is}")
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
                    # print(json_response)
                    break
                for element in json_response["data"]:
                    if element['id'] == iduu and element['status'] == "SUCCESS":
                        flag = False
        if flag:
            return None, None
        response = requests.get(url, headers=headers)
        return list(map(lambda x: x.split(';'), response.content.decode("utf-8")))
