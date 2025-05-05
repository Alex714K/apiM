import pandas
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
    # Константы
    MISSING_JSON_FILE = "Missing json file"

    def __init__(self, lock_ozon_request: RLock):
        self.lock_ozon_request = lock_ozon_request
        self.logger = getLogger("RequestOzon")

    def start(self, name_of_sheet: str, who_is: str):
        match name_of_sheet:
            case "analytics":
                return self.analytics(who_is)
            case "stock_on_warehouses":
                return self.stock_on_warehouses(name_of_sheet, who_is)
            case "stocks_FBS":
                return self.stocks_fbs(name_of_sheet, who_is)
            case "products":
                return self.products(name_of_sheet, who_is)
            case "prices":
                return self.prices(who_is)
            case "statistics":
                return self.statistics(who_is)
            case "statistics_product":
                return self.statistics_product(who_is)
            case "orders_alt":
                return self.orders_alt(who_is)
            case "sendings":
                return self.sendings(who_is)
            case "orders_1mnth", "orders_1week", "orders_2days":
                return self.orders(name_of_sheet, who_is)
        return None

    def statistics(self, who_is):
        self.check_token(who_is)
        # не допилено
        # url = 'https://performance.ozon.ru:443/api/client/campaign'
        # response = requests.get(url=url, headers=headers)
        # json_response = response.json()
        # # print(json_response)

    def check_token(self, who_is):
        pass
        # не допилено
        # with open("plugins/Ozon/data/token_and_time.txt", 'r') as txt:
        #     data = dict(map(lambda x: x.split('='), txt.read().split('\n')))
        # time_in_file = datetime.datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
        # time_now = datetime.datetime.today() + datetime.timedelta(seconds=1)
        # if time_in_file > time_now:
        #     return data['token']
        # else:
        #     url = 'https://performance.ozon.ru/api/client/token'
        #     headers = {
        #         "Content-Type:": "application/json",
        #         "Accept": "application/json"
        #     }
        #     params = {
        #         "client_id": ...,
        #         "client_secret": ...,
        #         "grant_type": "client_credentials"
        #     }
        #     response = requests.post(url=url, headers=headers)

    def sendings(self, who_is: str):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v2/posting/fbo/list"
        params = {
            "filter": {
                "since": (datetime.datetime.today() - datetime.timedelta(days=5)).isoformat()[:-4] + "Z",
                "to": (datetime.datetime.today()).isoformat()[:-4] + "Z"
            },
            "with": {
                "analytics_data": False,
                "financial_data": True
            },
            "limit": 1000,
            "offset": 0
        }

        data = list()
        for i in range(6):
            params["filter"]["since"] = (datetime.datetime.today() - datetime.timedelta(days=i*5+5)).isoformat()[:-4] + "Z"
            params["filter"]["to"] = (datetime.datetime.today() - datetime.timedelta(days=i*5)).isoformat()[:-4] + "Z"
            while True:
                try:
                    response = requests.post(url=url, headers=headers, json=params)
                except socket.gaierror:
                    self.logger.warning("gaierror in request (sendings)")
                    return 'Проблема с соединением'

                if not response:
                    self.logger.warning(f"sendings - Http статус: {response.status_code} ( {response.reason} )")
                    return response.status_code, response.reason

                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error("Missing json file in sendings")
                    return self.MISSING_JSON_FILE
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: sendings")
                data.extend(json_response["result"])

                if len(json_response["result"]) == 1000:
                    params["offset"] += 1000
                    time.sleep(5)
                else:
                    break

        return data

    @staticmethod
    def get_additional_sendings(who_is: str, posting_number: str) -> tuple[str, str] | str:
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v2/posting/fbo/get"
        params = {
            "posting_number": posting_number,
            "with": {
                "analytics_data": False,
                "financial_data": True
            }
        }
        while True:
            try:
                response = requests.post(url=url, headers=headers, json=params)
            except socket.gaierror:
                # self.logger.warning(f"gaierror in request (sendings)")
                return 'Проблема с соединением'
            if not response:
                # self.logger.warning(f"sendings - Http статус: {response.status_code} ( {response.reason} )")
                return RequestOzon.get_additional_sendings(who_is, posting_number)
            else:
                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    # self.logger.error(f"Missing json file in sendings")
                    return RequestOzon.MISSING_JSON_FILE
                # self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: sendings")
                if (len(json_response["result"]["financial_data"]["cluster_from"]) > 0 and
                        len(json_response["result"]["financial_data"]["cluster_to"]) > 0):
                    return (json_response["result"]["financial_data"]["cluster_from"],
                            json_response["result"]["financial_data"]["cluster_to"])

    def orders_alt(self, who_is: str):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v1/report/postings/create"

        params = {
            "filter": {
                "processed_at_from": (datetime.datetime.today() - datetime.timedelta(days=30)).isoformat()[:-4] + "Z",
                "processed_at_to": (datetime.datetime.today() - datetime.timedelta(days=1)).isoformat()[:-4] + "Z",
                "delivery_schema": ["fbo"]
            },
            "language": "RU"}
        try:
            response = requests.post(url=url, headers=headers, json=params)
        except socket.gaierror:
            self.logger.warning("gaierror in request (orders_alt_1)")
            return 'Проблема с соединением'
        if not response:
            self.logger.warning(f"orders_alt_1 - Http статус: {response.status_code} ( {response.reason} )")
            return response.status_code, response.reason

        try:
            # Преобразуем ответ в json-объект
            json_response = response.json()
        except requests.exceptions.JSONDecodeError:
            self.logger.error("Missing json file in orders_alt_1")
            return self.MISSING_JSON_FILE
        self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: orders_alt_1")
        code = json_response["result"]["code"]

        url = "https://api-seller.ozon.ru/v1/report/info"
        params = {"code": code}
        while True:
            try:
                response = requests.post(url=url, headers=headers, json=params)
            except socket.gaierror:
                self.logger.warning("gaierror in request (orders_alt_2)")
                return 'Проблема с соединением'

            if not response:
                self.logger.warning(f"orders_alt_2 - Http статус: {response.status_code} ( {response.reason} )")
                return response.status_code, response.reason

            try:
                # Преобразуем ответ в json-объект
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error("Missing json file in orders_alt_2")
                return self.MISSING_JSON_FILE
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: orders_alt_2")

            if json_response["result"]["status"] == "success":
                url = json_response["result"]["file"]
                break
            elif json_response["result"]["status"] == "failed":
                return 400, "failed"
            else:
                time.sleep(5)

        csv_data = pandas.read_csv(url, sep=";")
        return csv_data

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
        json_data = list()
        actual_distance = 0
        while True:
            params["offset"] = actual_distance
            try:
                response = requests.post(url=url, headers=headers, json=params)
            except socket.gaierror:
                self.logger.warning(f"gaierror in request ({name_of_sheet})")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"{name_of_sheet} - Http статус: {response.status_code} ( {response.reason} )")
                time.sleep(10)
            else:
                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error(f"Missing json file in {name_of_sheet}")
                    return self.MISSING_JSON_FILE
                # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                # Записываем данные в файл (убирать комментарий при необходимости)
                # with open('data.json', 'w', encoding='UTF-8') as d:
                #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                #     json.dump(json_response, d, ensure_ascii=False, indent=4)
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {name_of_sheet}")
                len_of_data = len(json_response["result"]["data"])
                json_data.extend(json_response["result"]["data"])
                if len_of_data < 1000:
                    break
                actual_distance += len_of_data
                time.sleep(60)
        return json_data

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
            return 'Проблема с соединением'
        if not response:
            self.logger.warning(f"{name_of_sheet} - Http статус: {response.status_code} ( {response.reason} )")
            return response.status_code, response.reason

        try:
            json_response = response.json()
        except requests.exceptions.JSONDecodeError:
            self.logger.error(f"Missing json file in {name_of_sheet}")
            return self.MISSING_JSON_FILE

        self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {name_of_sheet}")
        code_of_report = json_response["result"]["code"]
        time.sleep(5)
        url = "https://api-seller.ozon.ru/v1/report/info"
        params = {
            "code": code_of_report
        }

        while True:
            try:
                response = requests.post(url=url, headers=headers, json=params)
            except socket.gaierror:
                self.logger.error(f"gaierror {name_of_sheet}")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"{name_of_sheet} - Http статус: {response.status_code} ( {response.reason} )")
                time.sleep(10)
            else:
                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error(f"Missing json file in {name_of_sheet}")
                    return self.MISSING_JSON_FILE
                # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                # Записываем данные в файл (убирать комментарий при необходимости)
                # with open('data.json', 'w', encoding='UTF-8') as d:
                #     # # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                #     json.dump(json_response, d, ensure_ascii=False, indent=4)
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {name_of_sheet}")
            if json_response["result"]["status"] == "success":
                break
            else:
                time.sleep(5)
        url = json_response["result"]["file"]
        response = requests.get(url)
        file = response.content.decode()
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
            self.logger.warning(f"gaierror in request ({name_of_sheet})")
            return 'Проблема с соединением'
        if not response1:
            self.logger.warning(f"{name_of_sheet} - Http статус: {response1.status_code} ( {response1.reason} )")
            return response1.status_code, response1.reason
        else:
            try:
                json_response1 = response1.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {name_of_sheet}")
                return self.MISSING_JSON_FILE
            self.logger.debug(f"Http статус: {response1.status_code}, name_of_sheet: {name_of_sheet}")
            first_part = json_response1["result"]["rows"]

        # Второй запрос
        time.sleep(5)
        try:
            response2 = requests.post(url, headers=headers, json=params2)
        except socket.gaierror:
            self.logger.warning(f"gaierror in request ({name_of_sheet})")
            return 'Проблема с соединением'
        if not response2:
            self.logger.warning(f"{name_of_sheet} - Http статус: {response2.status_code} ( {response2.reason} )")
            return response2.status_code, response2.reason
        else:
            try:
                json_response2 = response2.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error(f"Missing json file in {name_of_sheet}")
                return self.MISSING_JSON_FILE
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
        # Первый запрос
        while True:
            try:
                response = requests.post(url, headers=headers, json=params1)
            except socket.gaierror:
                self.logger.warning("gaierror in request (analytics)")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"analytics - Http статус: {response.status_code} ( {response.reason} )")
                time.sleep(10)
            else:
                try:
                    # Преобразуем ответ в json-объект
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error("Missing json file in analytics")
                    return self.MISSING_JSON_FILE

                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: analytics")
                first_part = numpy.array(json_response["result"]["data"])
                parts["first"] = numpy.concatenate((parts["first"], first_part), axis=0)
                if len(json_response["result"]["data"]) != 1000:
                    break
                time.sleep(60)
                params1["offset"] += 1000
        time.sleep(60)

        # Второй запрос
        while True:
            try:
                response = requests.post(url, headers=headers, json=params2)
            except socket.gaierror:
                self.logger.warning("gaierror in request (analytics)")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"analytics - Http статус: {response.status_code} ( {response.reason} )")
                time.sleep(10)
            else:
                try:
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error("Missing json file in analytics")
                    return self.MISSING_JSON_FILE
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: analytics")
                second_part = numpy.array(json_response["result"]["data"])
                parts["second"] = numpy.concatenate((parts["second"], second_part), axis=0)
                if len(json_response["result"]["data"]) != 1000:
                    break
                time.sleep(60)
                params2["offset"] += 1000
        parts = {
            "first": parts["first"].tolist(),
            "second": parts["second"].tolist()
        }
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
            return parts["first"]
        parts.clear()
        return self.analytics(who_is=who_is)

    def prices(self, who_is: str):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v5/product/info/prices"
        last_id = ""
        file = list()
        while True:
            params = {
                "limit": 1000,
                "cursor": last_id,
                "filter": {"visibility": "ALL"}
            }
            try:
                response = requests.post(url=url, headers=headers, json=params)
            except socket.gaierror:
                self.logger.warning("gaierror in request (prices)")
                return 'Проблема с соединением'

            if not response:
                self.logger.warning(f"prices - Http статус: {response.status_code} ( {response.reason} )")
                return response.status_code, response.reason

            try:
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error("Missing json file in prices")
                return self.MISSING_JSON_FILE
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: prices")
            file.extend(json_response["items"])
            if len(json_response["items"]) == 1000:
                last_id = json_response["cursor"]
            else:
                break
        return file

    def statistics_product(self, who_is):
        token = self.get_token(who_is)
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        url = ("""https://performance.ozon.ru:443/api/client/statistics/campaign/product/json?
                dateFrom=2024-08-01&dateTo=2024-08-03""")
        try:
            response = requests.get(url, headers=headers)
        except socket.gaierror:
            self.logger.warning("gaierror in request (statistics_product)")
            return 'Проблема с соединением'
        if not response:
            self.logger.warning(f"statistics_product - Http статус: {response.status_code} ( {response.reason} )")
            time.sleep(2)
            return self.statistics_product(who_is)

        try:
            json_response = response.json()
        except requests.exceptions.JSONDecodeError:
            self.logger.error("Missing json file in statistics_product")
            time.sleep(5)
            return self.statistics_product(who_is)
        self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: statistics_product")

        return json_response

    def get_list_of_campaigns_id(self, who_is):
        headers = {
            "Authorization": self.get_token(who_is),
            "Content-Type": "application/json",
        }
        try:
            response = requests.get("https://performance.ozon.ru:443/api/client/campaign?advObjectType=SKU",
                                    headers=headers)
        except socket.gaierror:
            self.logger.warning("gaierror in request (get_list_of_campaigns_id)")
            return 'Проблема с соединением'
        if not response:
            self.logger.warning(f"get_list_of_campaigns_id - Http статус: {response.status_code} ( {response.reason} )")
            time.sleep(2)
            return self.get_list_of_campaigns_id(who_is)
        else:
            try:
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                self.logger.error("Missing json file in get_list_of_campaigns_id")
                time.sleep(5)
                return self.get_list_of_campaigns_id(who_is)
            self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: get_list_of_campaigns_id")
            return json_response

    def get_report(self, who_is: str, uuid: str):
        """
        Получение отчёта о рекламных компаниях
        """
        headers = {
            "Authorization": self.get_token(who_is),
            "Content-Type": "application/json",
        }
        while True:
            try:
                response = requests.get(f"https://performance.ozon.ru:443/api/client/statistics/{uuid}",
                                        headers=headers)
            except socket.gaierror:
                self.logger.warning("gaierror in request (get_report)")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"get_report - Http статус: {response.status_code} ( {response.reason} )")
                time.sleep(2)
                return self.get_report(who_is, uuid)
            else:
                try:
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error("Missing json file in get_report")
                    time.sleep(5)
                    return self.get_report(who_is, uuid)
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: get_report")
            match json_response["state"]:
                case "OK":
                    break
                case "ERROR":
                    self.logger.warning(f"get_token, Error:{json_response['error']}")
                    return self.get_report(who_is, uuid)

        params = {"UUID": uuid}
        try:
            response = requests.get("https://performance.ozon.ru:443/api/client/statistics/report",
                                    headers=headers,
                                    json=params)
        except socket.gaierror:
            self.logger.warning("gaierror in request (get_report)")
            time.sleep(2)
            return self.get_report(who_is, uuid)
        if not response:
            self.logger.warning(f"get_report - Http статус: {response.status_code} ( {response.reason} )")
            time.sleep(2)
            return self.get_report(who_is, uuid)

        try:
            json_response = response.json()
        except requests.exceptions.JSONDecodeError:
            self.logger.error("Missing json file in get_report")
            time.sleep(5)
            return self.get_report(who_is, uuid)
        self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: get_report")

        return json_response

    def get_token(self, who_is: str):
        """
        Получение токена
        :return: f"{token_type} {token}"
        """
        try:
            in_file_plus_secs = (
                    datetime.datetime.strptime(
                        os.getenv(f"Ozon-time_expire-{who_is}"), "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=2)
            )
        except TypeError as err:
            self.logger.warning(err)
        else:
            if in_file_plus_secs <= datetime.datetime.today():
                return os.getenv(f"Ozon-access_token-{who_is}")
        mail = os.getenv(f"Ozon-mail-{who_is}")
        secret = os.getenv(f"Ozon-secret-{who_is}")
        host = "https://performance.ozon.ru"
        endpoint = "/api/client/token"
        url = host + endpoint
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        params = {
            "client_id": mail,
            "client_secret": secret,
            "grant_type": "client_credentials"
        }
        try:
            response = requests.post(url, headers=headers, json=params)
        except socket.gaierror:
            self.logger.warning("gaierror in request (get_token)")
            time.sleep(5)
            return self.get_token(who_is)
        if not response:
            self.logger.warning(f"get_token - Http статус: {response.status_code} ( {response.reason} )")
            time.sleep(5)
            return self.get_token(who_is)

        try:
            json_response = response.json()
        except requests.exceptions.JSONDecodeError:
            self.logger.error("Missing json file in get_token")
            time.sleep(5)
            return self.get_token(who_is)
        self.logger.debug(f"Http статус: {response.status_code}, func: get_token")

        token = json_response["access_token"]
        token_type = json_response["token_type"]
        name = f"Ozon-time_expire-{who_is}"
        expire_time = datetime.datetime.today() + datetime.timedelta(seconds=int(json_response["expires_in"]))
        os.putenv(name, expire_time.strftime("%Y-%m-%d %H:%M:%S"))
        os.putenv(f"Ozon-access_token-{who_is}", f"{token_type} {token}")
        return f"{token_type} {token}"

    def stocks_fbs(self, name_of_sheet, who_is):
        headers = {
            "Client-Id": os.getenv(f"Ozon-Client_Id-{who_is}"),
            "Api-Key": os.getenv(f"Ozon-Api_Key-{who_is}")
        }
        url = "https://api-seller.ozon.ru/v4/product/info/stocks"
        params = {
            "cursor": "",
            "filter": {},
            "limit": 1000
        }

        result = list()
        flag = False
        while not flag:
            try:
                response = requests.post(url, headers=headers, json=params)
            except socket.gaierror:
                self.logger.warning(f"gaierror in request ({name_of_sheet})")
                return 'Проблема с соединением'
            if not response:
                self.logger.warning(f"{name_of_sheet} - Http статус: {response.status_code} ( {response.reason} )")
                time.sleep(2)
                return self.stocks_fbs(name_of_sheet, who_is)
            else:
                try:
                    json_response = response.json()
                except requests.exceptions.JSONDecodeError:
                    self.logger.error("Missing json file in get_report")
                    time.sleep(5)
                    return self.stocks_fbs(name_of_sheet, who_is)
                self.logger.debug(f"Http статус: {response.status_code}, name_of_sheet: {name_of_sheet}")

                result.extend(json_response["items"])

                if json_response["total"] < 1000:
                    flag = True

                params["cursor"] = json_response["cursor"]

        return result
