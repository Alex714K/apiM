import logging
import schedule
import time
from plugins.Api import Api


def Ozon_cycle():
    API = Api()
    # grand
    schedule.every(15).minutes.do(API.start, 'prices', 'grand', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'sendings', 'grand', 'Ozon')

    # terehov
    schedule.every(15).minutes.do(API.start, 'prices', 'terehov', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', 'terehov', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'sendings', 'terehov', 'Ozon')

    # dnk
    schedule.every(15).minutes.do(API.start, 'prices', 'dnk', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', 'dnk', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'sendings', 'dnk', 'Ozon')

    # 2ruz
    schedule.every(15).minutes.do(API.start, 'prices', '2ruz', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', '2ruz', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'sendings', '2ruz', 'Ozon')

    # peco
    schedule.every(15).minutes.do(API.start, 'prices', 'peco', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'stock_on_warehouses', 'peco', 'Ozon')
    schedule.every(30).minutes.do(API.start, 'sendings', 'peco', 'Ozon')

    # grand
    schedule.every().day.at('06:40').do(API.start, 'orders_alt', 'grand', 'Ozon')
    schedule.every().day.at('06:45').do(API.start, 'analytics', 'grand', 'Ozon')
    schedule.every().day.at('06:50').do(API.start, 'products', 'grand', 'Ozon')
    schedule.every().day.at('06:55').do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    schedule.every().day.at('07:00').do(API.start, 'orders_1week', 'grand', 'Ozon')
    schedule.every().day.at('07:05').do(API.start, 'orders_2days', 'grand', 'Ozon')

    # terehov
    schedule.every().day.at('07:10').do(API.start, 'orders_alt', 'terehov', 'Ozon')
    schedule.every().day.at('07:15').do(API.start, 'products', 'terehov', 'Ozon')
    schedule.every().day.at('07:20').do(API.start, 'orders_1mnth', 'terehov', 'Ozon')
    schedule.every().day.at('07:25').do(API.start, 'orders_1week', 'terehov', 'Ozon')
    schedule.every().day.at('07:30').do(API.start, 'orders_2days', 'terehov', 'Ozon')

    # dnk
    schedule.every().day.at('07:35').do(API.start, 'orders_alt', 'dnk', 'Ozon')
    schedule.every().day.at('07:40').do(API.start, 'products', 'dnk', 'Ozon')
    schedule.every().day.at('07:45').do(API.start, 'orders_1mnth', 'dnk', 'Ozon')
    schedule.every().day.at('07:50').do(API.start, 'orders_1week', 'dnk', 'Ozon')
    schedule.every().day.at('07:55').do(API.start, 'orders_2days', 'dnk', 'Ozon')

    # 2ruz
    schedule.every().day.at('08:00').do(API.start, 'orders_alt', '2ruz', 'Ozon')
    schedule.every().day.at('08:05').do(API.start, 'products', '2ruz', 'Ozon')
    schedule.every().day.at('08:10').do(API.start, 'orders_1mnth', '2ruz', 'Ozon')
    schedule.every().day.at('08:15').do(API.start, 'orders_1week', '2ruz', 'Ozon')
    schedule.every().day.at('08:20').do(API.start, 'orders_2days', '2ruz', 'Ozon')

    # peco
    schedule.every().day.at('08:25').do(API.start, 'orders_alt', 'peco', 'Ozon')
    schedule.every().day.at('08:30').do(API.start, 'products', 'peco', 'Ozon')
    schedule.every().day.at('08:35').do(API.start, 'orders_1mnth', 'peco', 'Ozon')
    schedule.every().day.at('08:40').do(API.start, 'orders_1week', 'peco', 'Ozon')
    schedule.every().day.at('08:45').do(API.start, 'orders_2days', 'peco', 'Ozon')

    logging.getLogger("extraInfo").info("Ozon scheduled")
