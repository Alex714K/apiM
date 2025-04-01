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
    schedule.every(10).minutes.do(API.start, 'prices', '2ruz', 'Ozon')
    # Остатки
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', 'terehov', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', 'dnk', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', '2ruz', 'Ozon')
    # Sendings
    schedule.every(30).minutes.do(API.start, 'sendings', 'grand', 'Ozon')
    # Orders_alt
    schedule.every().hour.do(API.start, 'orders_alt', 'grand', 'Ozon')
    schedule.every().hour.do(API.start, 'orders_alt', 'terehov', 'Ozon')
    schedule.every().hour.do(API.start, 'orders_alt', 'dnk', 'Ozon')
    schedule.every().hour.do(API.start, 'orders_alt', '2ruz', 'Ozon')
    # Утро гранд
    schedule.every().day.at("02:00").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("02:35").do(API.start, 'products', 'grand', 'Ozon')
    schedule.every().day.at("02:40").do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    schedule.every().day.at("02:45").do(API.start, 'orders_1week', 'grand', 'Ozon')
    schedule.every().day.at("02:50").do(API.start, 'orders_2days', 'grand', 'Ozon')
    # Вечер гранд
    schedule.every().day.at("08:00").do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at("08:30").do(API.start, 'products', 'grand', 'Ozon')
    schedule.every().day.at("08:35").do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    schedule.every().day.at("08:40").do(API.start, 'orders_1week', 'grand', 'Ozon')
    schedule.every().day.at("08:45").do(API.start, 'orders_2days', 'grand', 'Ozon')
    # Утро терехов
    # schedule.every().day.at("02:55").do(API.start, 'analytics', 'terehov', 'Ozon')
    schedule.every().day.at("03:05").do(API.start, 'products', 'terehov', 'Ozon')
    schedule.every().day.at("03:10").do(API.start, 'orders_1mnth', 'terehov', 'Ozon')
    schedule.every().day.at("03:15").do(API.start, 'orders_1week', 'terehov', 'Ozon')
    schedule.every().day.at("03:20").do(API.start, 'orders_2days', 'terehov', 'Ozon')
    # Вечер терехов
    # schedule.every().day.at("08:50").do(API.start, 'analytics', 'terehov', 'Ozon')
    schedule.every().day.at("09:00").do(API.start, 'products', 'terehov', 'Ozon')
    schedule.every().day.at("09:05").do(API.start, 'orders_1mnth', 'terehov', 'Ozon')
    schedule.every().day.at("09:10").do(API.start, 'orders_1week', 'terehov', 'Ozon')
    schedule.every().day.at("09:15").do(API.start, 'orders_2days', 'terehov', 'Ozon')
    # Утро днк
    # schedule.every().day.at("03:25").do(API.start, 'analytics', 'dnk', 'Ozon')
    schedule.every().day.at("03:35").do(API.start, 'products', 'dnk', 'Ozon')
    schedule.every().day.at("03:40").do(API.start, 'orders_1mnth', 'dnk', 'Ozon')
    schedule.every().day.at("03:45").do(API.start, 'orders_1week', 'dnk', 'Ozon')
    schedule.every().day.at("03:50").do(API.start, 'orders_2days', 'dnk', 'Ozon')
    # Вечер днк
    # schedule.every().day.at("09:20").do(API.start, 'analytics', 'dnk', 'Ozon')
    schedule.every().day.at("09:30").do(API.start, 'products', 'dnk', 'Ozon')
    schedule.every().day.at("09:35").do(API.start, 'orders_1mnth', 'dnk', 'Ozon')
    schedule.every().day.at("09:40").do(API.start, 'orders_1week', 'dnk', 'Ozon')
    schedule.every().day.at("09:45").do(API.start, 'orders_2days', 'dnk', 'Ozon')
    # Утро 2ruz
    # schedule.every().day.at("03:55").do(API.start, 'analytics', '2ruz', 'Ozon')
    schedule.every().day.at("04:00").do(API.start, 'products', '2ruz', 'Ozon')
    schedule.every().day.at("04:05").do(API.start, 'orders_1mnth', '2ruz', 'Ozon')
    schedule.every().day.at("04:10").do(API.start, 'orders_1week', '2ruz', 'Ozon')
    schedule.every().day.at("04:15").do(API.start, 'orders_2days', '2ruz', 'Ozon')
    # Вечер 2ruz
    # schedule.every().day.at("09:50").do(API.start, 'analytics', '2ruz', 'Ozon')
    schedule.every().day.at("09:55").do(API.start, 'products', '2ruz', 'Ozon')
    schedule.every().day.at("10:00").do(API.start, 'orders_1mnth', '2ruz', 'Ozon')
    schedule.every().day.at("10:05").do(API.start, 'orders_1week', '2ruz', 'Ozon')
    schedule.every().day.at("10:10").do(API.start, 'orders_2days', '2ruz', 'Ozon')

    logging.getLogger("extraInfo").info("Ozon scheduled")
