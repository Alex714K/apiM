import schedule
from Api import Api


def Ozon_cycle():
    API = Api()
    # Утро гранд
    schedule.every().day.at("01:30").do(API.start, 'analytics', 'grand', 'Ozon')
