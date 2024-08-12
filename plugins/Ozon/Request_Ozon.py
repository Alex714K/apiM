import datetime
import os
import socket
from threading import RLock
import time
import requests
import calendar
import numpy
from logging import getLogger


class RequestOzon:
    def __init__(self, LockOzonRequest: RLock):
        self.LockOzonRequest = LockOzonRequest
        self.logger = getLogger("RequestOzon")

    def start(self, name_of_sheet: str, who_is: str):
        match name_of_sheet:
            case 'analytics':
                return self.analytics(who_is)
            case 'stock_on_warehouses':
                return self.stock_on_warehouses(name_of_sheet, who_is)
            case 'products':
                return self.products(name_of_sheet, who_is)
            case 'prices':
                return self.prices(who_is)
            case 'statistics':
                return self.statistics(who_is)
        if name_of_sheet in ["orders_1mnth", "orders_1week", "orders_2days"]:
            return self.orders(name_of_sheet, who_is)

    def statistics(self, who_is):
        self.check_token()
        # url = 'https://performance.ozon.ru:443/api/client/campaign'
        # response = requests.get(url=url, headers=headers)
        # json_response = response.json()
        # # print(json_response)

    def check_token(self):
        with open("plugins/Ozon/data/token_and_time.txt", 'r') as txt:
            data = dict(map(lambda x: x.split('='), txt.read().split('\n')))
        time_in_file = datetime.datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        time_now = datetime.datetime.today() + datetime.timedelta(seconds=1)
        if time_in_file > time_now:
            # print('lol')
            return data['token']
        else:
            url = 'https://performance.ozon.ru/api/client/token'
            headers = {
                "Content-Type:": "application/json",
                "Accept": "application/json"
            }
            params = {
                "client_id": ...,
                "client_secret": ...,
                "grant_type": "client_credentials"
            }
            response = requests.post(url=url, headers=headers)

    def orders(self, name_of_sheet: str, who_is: str):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v1/analytics/data"
        today = datetime.date.today()
        match name_of_sheet:
            case 'orders_1mnth':
                date_from = today - datetime.timedelta(days=30)
            case 'orders_1week':
                date_from = today - datetime.timedelta(days=7)
            case 'orders_2days':
                date_from = today - datetime.timedelta(days=2)
            case _:
                date_from = today
        params = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "metrics": ["ordered_units"],
            "dimension": [
                "sku", "day"
            ],
            "limit": 1000
        }
        try:
            response = requests.post(url=url, headers=headers, json=params)
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({name_of_sheet})")
            return 'Проблема с соединением'
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
                self.logger.error(f"Missing json file in {name_of_sheet}")
                return 'Missing json file'
            # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response, d, ensure_ascii=False, indent=4)
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {name_of_sheet}")
            return json_response

    def products(self, name_of_sheet: str, who_is: str):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v1/report/products/create"
        params = {
            "language": "RU",
            "visibility": "ALL"
        }
        try:
            response = requests.post(url=url, headers=headers, json=params)
        except socket.gaierror:
            self.logger.error(f"gaierror {name_of_sheet}")
            # print(f"The 'gaierror' has come ({name_of_sheet})!\n")
            return 'Проблема с соединением'
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
                self.logger.error(f"Missing json file in {name_of_sheet}")
                return 'Missing json file'
            # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response, d, ensure_ascii=False, indent=4)
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {name_of_sheet}")
        code_of_report = json_response["result"]["code"]
        time.sleep(5)
        url = "https://api-seller.ozon.ru/v1/report/info"
        params = {
            "code": code_of_report
        }
        try:
            response = requests.post(url=url, headers=headers, json=params)
        except socket.gaierror:
            self.logger.error(f"gaierror {name_of_sheet}")
            # print(f"The 'gaierror' has come ({name_of_sheet})!\n")
            return 'Проблема с соединением'
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
                self.logger.error(f"Missing json file in {name_of_sheet}")
                return 'Missing json file'
            # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response, d, ensure_ascii=False, indent=4)
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {name_of_sheet}")
        url = json_response["result"]["file"]
        response = requests.get(url)
        file = list(map(lambda x: x[1:-1].split("\";\""), response.content.decode("utf-8-sig").split('\n')))
        return file

    def stock_on_warehouses(self, name_of_sheet: str, who_is: str):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v2/analytics/stock_on_warehouses"
        params1 = {
            "limit": 1000,
            "offset": 0
        }
        params2 = {
            "limit": 1000,
            "offset": 1000
        }

        # Выполняем запросы
        # Первый запрос
        try:
            response1 = requests.post(url, headers=headers, json=params1)
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({name_of_sheet})")
            return 'Проблема с соединением'
        if not response1:
            self.logger.warning(f"{name_of_sheet} - Http статус: {response1.status_code} ( {response1.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return response1.status_code, response1.reason
        else:
            try:
                # Преобразуем ответ в json-объект
                json_response1 = response1.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {name_of_sheet}")
                return
            # # print(json.dumps(json_response1, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response1, ensure_ascii=False, indent=4))
            #     json.dump(json_response1, d, ensure_ascii=False, indent=4)
            self.logger.debug(f"Http статус: {response1.status_code}, name_of_sheet: {name_of_sheet}")
            first_part = json_response1["result"]["rows"]

        # Второй запрос
        time.sleep(5)
        try:
            response2 = requests.post(url, headers=headers, json=params2)
        except socket.gaierror:
            self.logger.warning(f"gaierror with Google ({name_of_sheet})")
            return 'Проблема с соединением'
        if not response2:
            self.logger.warning(f"{name_of_sheet} - Http статус: {response2.status_code} ( {response2.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return response2.status_code, response2.reason
        else:
            try:
                # Преобразуем ответ в json-объект
                json_response2 = response2.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {name_of_sheet}")
                return 'Missing json file'
            # # print(json.dumps(json_response2, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response2, ensure_ascii=False, indent=4))
            #     json.dump(json_response2, d, ensure_ascii=False, indent=4)
            self.logger.debug(f"Http статус: {response2.status_code}, name_of_sheet: {name_of_sheet}")
            second_part = json_response2["result"]["rows"]
        first_part.extend(second_part)
        return first_part

    @staticmethod
    def make_params(name_of_sheet: str) -> dict | tuple[dict, dict] | None:
        match name_of_sheet:
            case _:
                params = None
        return params

    def analytics(self, who_is: str) -> tuple[int, str] | str:
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v1/analytics/data"
        today = datetime.date.today()
        if today.day == 1 and today.month == 1:
            date_from = datetime.date(today.year - 1, 12, 1)
            date_to = datetime.date(today.year - 1, 12, calendar.monthrange(today.year - 1, 12)[1])
        elif today.day == 1:
            date_from = datetime.date(today.year, today.month - 1, 1)
            date_to = datetime.date(today.year, today.month - 1, calendar.monthrange(today.year, today.month - 1)[1])
        else:
            date_from = datetime.date(today.year, today.month, 1)
            date_to = datetime.date(today.year, today.month, today.day)
        params1 = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "metrics": [
                "revenue", "ordered_units", "hits_view_search", "hits_view_pdp", "hits_view",
                "hits_tocart_search", "hits_tocart_pdp", "hits_tocart", "session_view_search"
            ],
            "dimension": [
                "sku", "day"
            ],
            "limit": 1000,
            "offset": 0
        }
        params2 = {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "metrics": [
                "session_view_pdp", "session_view", "conv_tocart_search", "conv_tocart_pdp", "conv_tocart", "returns",
                "cancellations", "delivered_units", "position_category"
            ],
            "dimension": [
                "sku", "day"
            ],
            "limit": 1000,
            "offset": 0
        }
        parts = {
            "first": numpy.array([]),
            "second": numpy.array([])
        }
        # Выполняем запросы
        while True:
            # Первый запрос
            try:
                response = requests.post(url, headers=headers, json=params1)
            except socket.gaierror:
                self.logger.warning(f"gaierror with Google (analytics)")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"analytics - Http статус: {response.status_code} ( {response.reason} )")
                # with open('data.json') as data:
                #     return json.load(data)
                return response.status_code, response.reason
            else:
                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error(f"Missing json file in analytics")
                    return 'Missing json file'
                # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                # Записываем данные в файл (убирать комментарий при необходимости)
                # with open('data.json', 'w', encoding='UTF-8') as d:
                #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                #     json.dump(json_response, d, ensure_ascii=False, indent=4)
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: analytics")
                first_part = numpy.array(json_response["result"]["data"])
                parts["first"] = numpy.concatenate((parts["first"], first_part), axis=0)
                # parts["first"].extend(first_part)
                if len(json_response["result"]["data"]) != 1000:
                    break
                time.sleep(60)
                params1["offset"] += 1000
        time.sleep(60)
        while True:
            # Второй запрос
            try:
                response = requests.post(url, headers=headers, json=params2)
            except socket.gaierror:
                self.logger.warning(f"gaierror with Google (analytics)")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"analytics - Http статус: {response.status_code} ( {response.reason} )")
                # with open('data.json') as data:
                #     return json.load(data)
                return response.status_code, response.reason
            else:
                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error(f"Missing json file in analytics")
                    return 'Missing json file'
                # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                # Записываем данные в файл (убирать комментарий при необходимости)
                # with open('data.json', 'w', encoding='UTF-8') as d:
                #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                #     json.dump(json_response, d, ensure_ascii=False, indent=4)
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: analytics")
                second_part = numpy.array(json_response["result"]["data"])
                parts["second"] = numpy.concatenate((parts["second"], second_part), axis=0)
                # parts["second"].extend(second_part)
                if len(json_response["result"]["data"]) != 1000:
                    break
                time.sleep(60)
                params2["offset"] += 1000
        parts["first"] = parts["first"].tolist()
        parts["second"] = parts["second"].tolist()
        ids_of_second_part = list(map(lambda x: [x["dimensions"][0]["id"], x["dimensions"][1]["id"]], parts["second"]))
        for ind in range(len(parts["first"])):
            id_in_first_part = [parts["first"][ind]["dimensions"][0]["id"], parts["first"][ind]["dimensions"][1]["id"]]
            try:
                metrics_in_second_part = parts["second"][ids_of_second_part.index(id_in_first_part)]["metrics"]
                parts["first"][ind]["metrics"].extend(metrics_in_second_part)
            except ValueError:
                self.logger.error("WTF - analytics, Ozon")
                break
        else:
            # # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data/data.json', 'w', encoding='UTF-8') as d:
            #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(parts["first"], d, ensure_ascii=False, indent=4)
            return parts["first"]
        parts = None
        return self.analytics(who_is=who_is)

    def prices(self, who_is: str):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v4/product/info/prices"
        last_id = ""
        file = list()
        while True:
            params = {
                "limit": 1000,
                "last_id": last_id,
                "filter": {"visibility": "ALL"}
            }
            try:
                response = requests.post(url=url, headers=headers, json=params)
            except socket.gaierror:
                self.logger.warning(f"gaierror with Google (prices)")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"prices - Http статус: {response.status_code} ( {response.reason} )")
                # with open('data.json') as data:
                #     return json.load(data)
                return response.status_code, response.reason
            else:
                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error(f"Missing json file in prices")
                    return 'Missing json file'
                # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                # Записываем данные в файл (убирать комментарий при необходимости)
                # with open('data.json', 'w', encoding='UTF-8') as d:
                #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                #     json.dump(json_response, d, ensure_ascii=False, indent=4)
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: prices")
            file.extend(json_response["result"]["items"])
            if len(json_response["result"]["items"]) == 1000:
                last_id = json_response["result"]["last_id"]
                # print(last_id)
            else:
                break
        return file
