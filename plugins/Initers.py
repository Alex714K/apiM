import logging
import datetime


class Initer:
    """
    Запускает логгинг.
    Класс для наследования
    """
    def __init__(self):
        self.parameters = None
        current_date = datetime.datetime.now()
        logging.basicConfig(level=logging.DEBUG, filename=f"data/logs/{current_date.strftime('%Y-%m')}.log",
                            filemode="w", format="%(asctime)s %(levelname)s %(message)s", encoding="UTF-8")

    def get_parameters(self):
        """Достаёт словарь параметров в all_urls.txt"""
        with open('Wildberries/data/all_urls.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
