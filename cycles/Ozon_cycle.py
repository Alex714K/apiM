import schedule
from Api import Api


def Ozon_cycle():
    API = Api()
    # Утро гранд
    schedule.every().day.at("01:30").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("01:35").do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every().day.at("01:40").do(API.start, 'products', 'grand', 'Ozon')
    schedule.every(10).minutes.do(API.start, 'prices', 'grand', 'Ozon')
    # Вечер гранд
    schedule.every().day.at("16:00").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("16:05").do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every().day.at("16:10").do(API.start, 'products', 'grand', 'Ozon')
