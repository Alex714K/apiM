import Logger
import logging
import datetime


class Initer:
    """
    ��������� �������.
    ����� ��� ������������
    """
    def __init__(self):
        self.parameters = None
        # self.logger = Logger.get_logger("Apister")
        current_date = datetime.datetime.now()
        logging.basicConfig(level=logging.DEBUG, filename=f"logs/{current_date.strftime('%m-%d-%y %H-%M-%S')}.log",
                            filemode="w", format="%(asctime)s %(levelname)s %(message)s", )

    def get_parameters(self):
        """������ ������� ���������� � all_urls.txt"""
        with open('data/all_urls.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))


class Getter:
    """
    ������ �� all_urls.txt ��� ������ � ���������� � self.parameters �������.
    ����� ��� ������������
    """
    def __init__(self):
        self.parameters = None
        self.get_parameters()

    def get_parameters(self):
        """������ ������� ���������� � all_urls.txt"""
        with open('data/all_urls.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
