import schedule
from Api import Api


def Ozon_cycle():
    API = Api()
    # Утро гранд
    schedule.every().day.at("01:30").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("01:35").do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
