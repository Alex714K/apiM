import Logger
import logging
import datetime


class Initer:
    def __init__(self):
        self.parameters = None
        # self.logger = Logger.get_logger("Apister")
        current_date = datetime.datetime.now()
        logging.basicConfig(level=logging.INFO, filename=f"{current_date.strftime('%m-%d-%y %H-%M-%S')}.log",
                            filemode="w", format="%(asctime)s %(levelname)s %(message)s")

    def get_parameters(self):
        """Достаёт словарь параметров в parameters.txt"""
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))


class Getter:
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    def get_parameters(self):
        """Достаёт словарь параметров в parameters.txt"""
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
