import Logger


class Initer:
    def __init__(self):
        self.parameters = None
        self.get_parameters()
        self.logger = Logger.get_logger("Apister")

    def get_parameters(self):
        """Достаёт словарь параметров в parameters.txt"""
        with open('parameters.txt', 'r') as txt:
            param = txt.read().split('\n')
        self.parameters = dict(map(lambda x: x.split('='), param))
