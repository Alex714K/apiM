import logging
import schedule
from plugins.Api import Api


def Ozon_cycle():
    API = Api()
    # Prices
    schedule.every(10).minutes.do(API.start, 'prices', 'grand', 'Ozon')
    # Утро гранд
    schedule.every().day.at("01:30").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("01:35").do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every().day.at("01:40").do(API.start, 'products', 'grand', 'Ozon')
    schedule.every().day.at("01:45").do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    schedule.every().day.at("01:50").do(API.start, 'orders_1week', 'grand', 'Ozon')
    schedule.every().day.at("01:55").do(API.start, 'orders_2days', 'grand', 'Ozon')
    # Вечер гранд
    schedule.every().day.at("16:00").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("16:05").do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every().day.at("16:10").do(API.start, 'products', 'grand', 'Ozon')
    schedule.every().day.at("16:15").do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    schedule.every().day.at("16:20").do(API.start, 'orders_1week', 'grand', 'Ozon')
    schedule.every().day.at("16:25").do(API.start, 'orders_2days', 'grand', 'Ozon')

    logging.getLogger("extraInfo").info("Ozon scheduled")
