import logging
import sys
import requests
import datetime
import json
from Initers import Getter


class RequestWildberries(Getter):
    def start(self, name_of_sheet: str, storage_paid=False, statements=False, **kwargs) -> (tuple[list | dict, int] |
                                                                                            None):
        """Формирует с отправляет запрос на сервера Wildberries для получения различных данных (в зависимости от
        вводимых параветров). При успешнов получении возвращает json-объект. При ошибке останавливает программу и
        пишет ошибку в консоль"""
        # Дата
        if storage_paid:
            kwargs['dateFrom'], date, kwargs['dateTo'] = self.choose_dates(dateFrom=kwargs['dateFrom'])
        elif statements:
            kwargs['dateFrom'], date, kwargs['dateTo'] = self.choose_dates(dateFrom=kwargs['dateFrom'])
        else:
            kwargs['dateFrom'], kwargs['date'], kwargs['dateTo'] = self.choose_dates(kwargs['dateFrom'], kwargs['date'],
                                                                                     kwargs['dateTo'])

        # Ссылка
        try:
            url = self.parameters[f"url_{name_of_sheet}"]
        except KeyError:
            logging.critical("Wrong name of sheet!")
            sys.exit("Wrong name of sheet!")
        # Ссылка запроса
        request = self.make_request(url, kwargs)
        # Токен
        with open('wildberries_token.txt', 'r') as txt:
            authorization = txt.read()
        headers = {
            'Authorization': authorization
        }

        # Выполняем запрос
        response = requests.get(request, headers=headers)
        if not response:
            logging.warning(f"Ошибка выполнения запроса:\nHttp статус: {response.status_code} ( {response.reason} )")
            print("Ошибка выполнения запроса:")
            print(request)
            print(f"Http статус: {response.status_code} ( {response.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return
        else:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл
            with open('data.json', 'w') as d:
                # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                json.dump(json_response, d, ensure_ascii=False, indent=4)
            logging.info(f"Http статус: {response.status_code}")
            print("Успешно")
            print(request)
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
    def choose_dates(dateFrom: str = None, date: str = None, dateTo: str = None) -> tuple[str, str, str]:
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
            case 'tariffs':
                with open('date_of_tariffs.txt', 'r') as txt:
                    date = txt.read()
            case 'statements':
                first_day = datetime.date.today().weekday() % 7 + 7
                last_day = first_day - 6
                dateFrom = datetime.date.today() - datetime.timedelta(days=first_day)
                dateTo = datetime.date.today() - datetime.timedelta(days=last_day)
            case 'storage_paid':
                date = datetime.date.today()
                year = date.year
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
                with open('date_of_tariffs.txt', 'r') as txt:
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
