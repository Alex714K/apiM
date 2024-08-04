import logging
import schedule
import time
from plugins.Api import Api


def Ozon_cycle():
    API = Api()
    # Prices
    schedule.every(10).minutes.do(API.start, 'prices', 'grand', 'Ozon')
    schedule.every(10).minutes.do(API.start, 'prices', 'terehov', 'Ozon')
    schedule.every(10).minutes.do(API.start, 'prices', 'dnk', 'Ozon')
    # Утро гранд
    schedule.every().day.at("02:25").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("02:30").do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every().day.at("02:35").do(API.start, 'products', 'grand', 'Ozon')
    schedule.every().day.at("02:40").do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    schedule.every().day.at("02:45").do(API.start, 'orders_1week', 'grand', 'Ozon')
    schedule.every().day.at("02:50").do(API.start, 'orders_2days', 'grand', 'Ozon')
    # Вечер гранд
    schedule.every().day.at("08:20").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("08:25").do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every().day.at("08:30").do(API.start, 'products', 'grand', 'Ozon')
    schedule.every().day.at("08:35").do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    schedule.every().day.at("08:40").do(API.start, 'orders_1week', 'grand', 'Ozon')
    schedule.every().day.at("08:45").do(API.start, 'orders_2days', 'grand', 'Ozon')
    # Утро гранд
    # schedule.every().day.at("02:55").do(API.start, 'analytics', 'terehov', 'Ozon')
    schedule.every().day.at("03:00").do(API.start, 'stock_on_warehouses', 'terehov', 'Ozon')
    schedule.every().day.at("03:05").do(API.start, 'products', 'terehov', 'Ozon')
    schedule.every().day.at("03:10").do(API.start, 'orders_1mnth', 'terehov', 'Ozon')
    schedule.every().day.at("03:15").do(API.start, 'orders_1week', 'terehov', 'Ozon')
    schedule.every().day.at("03:20").do(API.start, 'orders_2days', 'terehov', 'Ozon')
    # Вечер гранд
    # schedule.every().day.at("08:50").do(API.start, 'analytics', 'terehov', 'Ozon')
    schedule.every().day.at("08:55").do(API.start, 'stock_on_warehouses', 'terehov', 'Ozon')
    schedule.every().day.at("09:00").do(API.start, 'products', 'terehov', 'Ozon')
    schedule.every().day.at("09:05").do(API.start, 'orders_1mnth', 'terehov', 'Ozon')
    schedule.every().day.at("09:10").do(API.start, 'orders_1week', 'terehov', 'Ozon')
    schedule.every().day.at("09:15").do(API.start, 'orders_2days', 'terehov', 'Ozon')
    # Утро гранд
    # schedule.every().day.at("03:25").do(API.start, 'analytics', 'dnk', 'Ozon')
    schedule.every().day.at("03:30").do(API.start, 'stock_on_warehouses', 'dnk', 'Ozon')
    schedule.every().day.at("03:35").do(API.start, 'products', 'dnk', 'Ozon')
    schedule.every().day.at("03:40").do(API.start, 'orders_1mnth', 'dnk', 'Ozon')
    schedule.every().day.at("03:45").do(API.start, 'orders_1week', 'dnk', 'Ozon')
    schedule.every().day.at("03:50").do(API.start, 'orders_2days', 'dnk', 'Ozon')
    # Вечер гранд
    # schedule.every().day.at("09:20").do(API.start, 'analytics', 'dnk', 'Ozon')
    schedule.every().day.at("09:25").do(API.start, 'stock_on_warehouses', 'dnk', 'Ozon')
    schedule.every().day.at("09:30").do(API.start, 'products', 'dnk', 'Ozon')
    schedule.every().day.at("09:35").do(API.start, 'orders_1mnth', 'dnk', 'Ozon')
    schedule.every().day.at("09:40").do(API.start, 'orders_1week', 'dnk', 'Ozon')
    schedule.every().day.at("09:45").do(API.start, 'orders_2days', 'dnk', 'Ozon')

    logging.getLogger("extraInfo").info("Ozon scheduled")
