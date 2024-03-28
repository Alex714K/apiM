import sys
import requests
import datetime
import json


class RequestWildberries:
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    def start(self, name_of_sheet: str, dateFrom: str, date: str, flag: str, limit: str, dateTo: str, from_rk: str,
              to_rk: str) -> tuple[list | dict, int] | None:
        """Формирует с отправляет запрос на сервера Wildberries для получения различных данных (в зависимости от
        вводимых параветров). При успешнов получении возвращает json-объект. При ошибке останавливает программу и
        пишет ошибку в консоль"""
        # Дата
        dateFrom, date = self.choose_dates(dateFrom=dateFrom, date=date)
        # Ссылка
        try:
            url = self.parameters[f"url_{name_of_sheet}"]
        except KeyError:
            sys.exit('Wrong name of sheet!')
        # Ссылка запроса
        request = self.make_request(url, dateFrom=dateFrom, date=date, flag=flag, limit=limit, dateTo=dateTo,
                                    from_rk=from_rk, to_rk=to_rk)
        # Токен
        with open('wildberries_token.txt', 'r') as txt:
            authorization = txt.read()
        headers = {
            'Authorization': authorization
        }

        # Выполняем запрос
        response = requests.get(request, headers=headers)
        if not response:
            print("Ошибка выполнения запроса:")
            print(request)
            print(f"Http статус: {response.status_code} ( {response.reason} )")
            # with open('data.json') as data:
            #     return json.load(data)
            return None
        else:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            # Записываем данные в файл
            with open('data.json', 'w') as d:
                # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                json.dump(json_response, d, ensure_ascii=False, indent=4)
            print("Успешно")
            print(request)
            print(f'Http статус: {response.status_code}')
            return json_response, response.status_code

    @staticmethod
    def make_request(url, **kwargs) -> str:
        """Формируей ссылку для отправки запроса на сервер Wildberries"""
        if kwargs == {}:
            fin_url = f"{url}"
        else:
            fin_url = f"{url}?"
            a = 0
            for key, item in kwargs.items():
                if a == 0:
                    if item != None:
                        if 'rk' in key:
                            fin_url += f"{key[:-3]}={item}"
                        else:
                            fin_url += f"{key}={item}"
                        a += 1
                else:
                    if item != None:
                        if 'rk' in key:
                            fin_url += f"&{key[:-3]}={item}"
                        else:
                            fin_url += f"&{key}={item}"

        return fin_url

    def get_parameters(self):
        """Достаёт словарь параметров в parameters.txt"""
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))

    @staticmethod
    def choose_dates(dateFrom, date) -> tuple[str, str]:
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

        return dateFrom, date
