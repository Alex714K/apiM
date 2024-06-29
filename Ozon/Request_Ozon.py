import socket
import logging
import requests
import json
import numpy


class RequestOzon:
    def start(self, name_of_sheet: str, who_is: str):
        match name_of_sheet:
            case 'analytics':
                return self.analytics(who_is)

    @staticmethod
    def analytics(who_is: str) -> tuple[int, str] | str:
        headers = {}
        with open("Ozon/data/id's.txt") as txt:
            data = dict(map(lambda x: x.split('='), txt.read().split('\n')))
        for key, value in data.items():
            headers[key] = value
        url = "https://api-seller.ozon.ru/v1/analytics/data"
        params1 = {
            "date_from": "2024-06-27",
            "date_to": "2024-06-27",
            "metrics": [
                "revenue", "ordered_units", "hits_view_search", "hits_view_pdp", "hits_view",
                "hits_tocart_search", "hits_tocart_pdp", "hits_tocart", "session_view_search"
            ],
            "dimension": [
                "sku", "spu", "day"
            ],
            "limit": 1000
        }
        params2 = {
            "date_from": "2024-06-27",
            "date_to": "2024-06-27",
            "metrics": [
                "session_view_pdp", "session_view", "conv_tocart_search", "conv_tocart_pdp", "conv_tocart", "returns",
                "cancellations", "delivered_units", "position_category"
            ],
            "dimension": [
                "sku", "spu", "day"
            ],
            "limit": 1000
        }
        # Выполняем запросы
        # Первый запрос
        try:
            response1 = requests.post(url, headers=headers, json=params1)
        except socket.gaierror:
            logging.error("gaierror")
            logging.error("In Ozon")
            print('In Ozon')
            print("The 'gaierror' has come!\n")
            return 'Проблема с соединением'
        if not response1:
            logging.warning(f"Ошибка выполнения запроса:\nHttp статус: {response1.status_code} ( {response1.reason} )")
            print("Ошибка выполнения запроса:")
            print(url)
            print(f"Http статус: {response1.status_code} ( {response1.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return response1.status_code, response1.reason
        else:
            try:
                # Преобразуем ответ в json-объект
                json_response1 = response1.json()
            except requests.exceptions.JSONDecodeError:
                print('Missing json file')
                return 'Missing json file'
            # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response1, d, ensure_ascii=False, indent=4)
            logging.info(f"Http статус: {response1.status_code}")
            print("Успешно")
            print(url)
            print(f"Http статус: {response1.status_code}")
            first_part = json_response1["result"]["data"]

        # Второй запрос
        try:
            response2 = requests.post(url, headers=headers, json=params2)
        except socket.gaierror:
            logging.error("gaierror")
            logging.error("In Ozon")
            print('In Ozon')
            print("The 'gaierror' has come!\n")
            return 'Проблема с соединением'
        if not response2:
            logging.warning(f"Ошибка выполнения запроса:\nHttp статус: {response2.status_code} ( {response2.reason} )")
            print("Ошибка выполнения запроса:")
            print(url)
            print(f"Http статус: {response2.status_code} ( {response2.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return response2.status_code, response2.reason
        else:
            try:
                # Преобразуем ответ в json-объект
                json_response2 = response2.json()
            except requests.exceptions.JSONDecodeError:
                print('Missing json file')
                return 'Missing json file'
            # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл (убирать комментарий при необходимости)
            # with open('data.json', 'w', encoding='UTF-8') as d:
            #     # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            #     json.dump(json_response2, d, ensure_ascii=False, indent=4)
            logging.info(f"Http статус: {response2.status_code}")
            print("Успешно")
            print(url)
            print(f"Http статус: {response2.status_code}")
            second_part = json_response2["result"]["data"]

        ids_of_second_part = list(map(lambda x: x["dimensions"][0]["id"], second_part))
        for ind in range(len(first_part)):
            id_in_first_part = first_part[ind]["dimensions"][0]["id"]
            metrics_in_second_part = second_part[ids_of_second_part.index(id_in_first_part)]["metrics"]
            first_part[ind]["metrics"].extend(metrics_in_second_part)
            # Записываем данные в файл (убирать комментарий при необходимости)
        # with open('data.json', 'w', encoding='UTF-8') as d:
        #     # print(json.dumps(json_response, ensure_ascii=False, indent=4))
        #     json.dump(first_part, d, ensure_ascii=False, indent=4)
        return first_part
