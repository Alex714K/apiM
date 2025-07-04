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
    def __init__(self, lock_wb_request: RLock):
        self.name_of_sheet = None
        self.lock_wb_request = lock_wb_request
        self.logger = getLogger("RequestWildberries")

    def start(self, name_of_sheet: str, who_is: str):
        match name_of_sheet:
            case "stocks_hard":
                return self.stocks_hard(who_is)
            case "nm_report":
                return self.nm_report(who_is)
            case _:
                return self.simple_start(name_of_sheet, who_is)

    def simple_start(self, name_of_sheet: str, who_is: str):
        """Формирует и отправляет запрос на сервера Wildberries для получения различных данных (в зависимости от
        вводимых параметров). При успешном получении возвращает json-объект. При ошибке ничего не возвращает и
        пишет ошибку в консоль"""
        self.name_of_sheet = name_of_sheet
        # Ссылка
        url = os.getenv(f"Wildberries-url-{name_of_sheet}")
        if url is None:
            self.logger.critical(f"Man, you forget {name_of_sheet}1 in Request_wildberries.py")
            sys.exit(f"Man, you forget {name_of_sheet}1 in Request_wildberries.py")

        # Токен
        headers = {
            "Authorization": os.getenv(f"Wildberries-token-{who_is}")
        }

        # Выполняем запрос
        try:
            # Если только через ссылку
            if (name_of_sheet in ["stocks", "orders_1mnth", "orders_1week", "orders_2days", "orders_today"] or
                    name_of_sheet in ["sales_today", "sales_1mnth", "tariffs_boxes", "tariffs_pallet", "statements"] or
                    name_of_sheet in ["prices", "fixed_prices", "rk", "coefficients", "stat_prodvigene"]):
                params = self.make_params()
                url_for_reqst = self.make_request(url, params)
                response = requests.get(url_for_reqst, headers=headers)
            # Если через json и ссылку
            elif name_of_sheet in []:
                params = self.make_params()
                response = requests.get(url, headers=headers, json=params)
            else:
                self.logger.critical(f"Man, you forget {name_of_sheet}2 in Request_wildberries.py")
                sys.exit(f"Man, you forget {name_of_sheet}2 in Request_wildberries.py")
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({self.name_of_sheet})")
            return "Проблема с соединением"

        if not response:
            self.logger.warning(f"{name_of_sheet} - Http статус: {response.status_code} ( {response.reason} )")
            return response.status_code, response.reason
        else:
            try:
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {self.name_of_sheet}")
                return "Missing json file"
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

        count = 0

        while True:
            try:
                response = requests.get(url, headers=headers)
            except socket.gaierror:
                self.logger.warning(f"gaierror with Google ({self.name_of_sheet})")
                time.sleep(10)
                continue
            json_response = response.json()
            try:
                if json_response["data"]["status"] == "done":
                    break

                self.logger.debug(f"stocks_hard - status:{json_response["data"]["status"]}")
                if count < 4:
                    count += 1
                time.sleep(5 * count)
            except KeyError:
                self.logger.error(f"stocks_hard - status:{json_response}")
                time.sleep(4)
        url = f"https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/download"

        return {"json": self.try_get_data_of_hard_stocks(url, headers), "warehouses": self.get_warehouses(who_is)}, response.status_code

    def try_get_data_of_hard_stocks(self, url: str, headers: dict):
        try:
            response = requests.get(url, headers=headers)
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({self.name_of_sheet})")
            time.sleep(10)
            return self.try_get_data_of_hard_stocks(url, headers)

        if not response:
            self.logger.warning(f"stocks_hard - Http статус: {response.status_code} ( {response.reason} )")
            return self.try_get_data_of_hard_stocks(url, headers)
        else:
            try:
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {self.name_of_sheet}")
                return "Missing json file"
            if json_response is int and json_response != 200:
                return self.try_get_data_of_hard_stocks(url, headers)
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {self.name_of_sheet}")
            return json_response


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
        response_json = response.json()
        if response_json is dict and response_json["status"] == 401:
            sys.exit(f"get_warehouses - status: {response_json["status"]}")
        return list(map(lambda x: str(x["name"]).replace("(", "").replace(")", ""), response.json()))

    @staticmethod
    def make_request(url, kwargs: dict) -> str:
        """Формируей ссылку для отправки запроса на сервер Wildberries"""
        if kwargs == {}:
            return url

        fin_url = f"{url}?"
        a = True
        for key, item in kwargs.items():
            if a and item is not None:
                if 'rk' in key:
                    fin_url += f"{key[:-3]}={item}"
                else:
                    fin_url += f"{key}={item}"
                a = False
            elif item is not None:
                if 'rk' in key:
                    fin_url += f"&{key[:-3]}={item}"
                else:
                    fin_url += f"&{key}={item}"

        return fin_url

    @staticmethod
    def choose_dates_old(date_from: str = None, date: str = None, date_to: str = None) -> tuple[str, str, str]:
        """Если вводиться не дата, а слова: today, 2days, 1week, 1mnth; то выводятся сегодняшняя дата и до -30 дней"""
        match date_from:
            case 'today':
                date_from = datetime.date.today()
            case '2days':
                date_from = datetime.date.today() - datetime.timedelta(days=2)
            case '1week':
                date_from = datetime.date.today() - datetime.timedelta(weeks=1)
            case '1mnth':
                date_from = datetime.date.today() - datetime.timedelta(days=30)
            case 'statements':
                first_day = datetime.date.today().weekday() + 7
                last_day = first_day - 6
                date_from = datetime.date.today() - datetime.timedelta(days=first_day)
                date_to = datetime.date.today() - datetime.timedelta(days=last_day)
            case 'storage_paid':
                year = datetime.date.today().year
                month = (datetime.date.today() - datetime.timedelta(days=30)).month
                last_day = (datetime.date.today() - datetime.timedelta(days=1)).day
                date_from = datetime.date(year, month, 1).strftime("%Y-%m-%d")
                date_to = datetime.date(year, month, last_day).strftime("%Y-%m-%d")

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

        match date_to:
            case 'today':
                date_to = datetime.date.today()
            case '2days':
                date_to = datetime.date.today() - datetime.timedelta(days=2)
            case '1week':
                date_to = datetime.date.today() - datetime.timedelta(weeks=1)
            case '1mnth':
                date_to = datetime.date.today() - datetime.timedelta(days=30)
        return date_from, date, date_to

    def make_params(self) -> dict | dict[str, int] | dict[str, str]:
        match self.name_of_sheet:
            case 'stocks':
                params = {'dateFrom': '2024-03-25'}
            case 'orders_today':
                params = {
                    'dateFrom': datetime.date.today().strftime("%Y-%m-%d"),
                    'flag': 1
                }
            case 'sales_today':
                params = {
                    'dateFrom': datetime.date.today().strftime("%Y-%m-%d"),
                    'flag': 1
                }
            case 'sales_1mnth':
                params = {
                    'dateFrom': (datetime.date.today() - datetime.timedelta(days=31)).strftime("%Y-%m-%d"),
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
            case "coefficients":
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
        requests.post(url, headers=headers, json=params)
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

        return response.content.decode("utf-8"), response.status_code
