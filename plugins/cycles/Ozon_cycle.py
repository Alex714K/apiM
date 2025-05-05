import logging
import schedule
import time
from plugins.Api import Api


def ozon_cycle():
    API = Api()
    my_scheduler = schedule.Scheduler()
    # grand
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'grand', 'Ozon')
    my_scheduler.every(30).minutes.do(API.start, 'stock_on_warehouses', 'grand', 'Ozon')
    my_scheduler.every(30).minutes.do(API.start, 'sendings', 'grand', 'Ozon')

    # terehov
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'terehov', 'Ozon')
    my_scheduler.every(30).minutes.do(API.start, 'stock_on_warehouses', 'terehov', 'Ozon')

    # dnk
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'dnk', 'Ozon')
    my_scheduler.every(30).minutes.do(API.start, 'stock_on_warehouses', 'dnk', 'Ozon')

    # 2ruz
    my_scheduler.every(15).minutes.do(API.start, 'prices', '2ruz', 'Ozon')
    my_scheduler.every(30).minutes.do(API.start, 'stock_on_warehouses', '2ruz', 'Ozon')

    # peco
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'peco', 'Ozon')
    my_scheduler.every(30).minutes.do(API.start, 'stock_on_warehouses', 'peco', 'Ozon')

    # peco_bathroom
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'peco_bathroom', 'Ozon')
    my_scheduler.every(30).minutes.do(API.start, 'stock_on_warehouses', 'peco_bathroom', 'Ozon')

    # grand
    my_scheduler.every().day.at('07:10').do(API.start, 'orders_alt', 'grand', 'Ozon')
    my_scheduler.every().day.at('07:15').do(API.start, 'analytics', 'grand', 'Ozon')
    my_scheduler.every().day.at('07:20').do(API.start, 'products', 'grand', 'Ozon')
    my_scheduler.every().day.at('07:25').do(API.start, 'orders_1mnth', 'grand', 'Ozon')
    my_scheduler.every().day.at('07:30').do(API.start, 'orders_1week', 'grand', 'Ozon')
    my_scheduler.every().day.at('07:35').do(API.start, 'orders_2days', 'grand', 'Ozon')

    # terehov
    my_scheduler.every().day.at('07:40').do(API.start, 'orders_alt', 'terehov', 'Ozon')
    my_scheduler.every().day.at('07:45').do(API.start, 'products', 'terehov', 'Ozon')
    my_scheduler.every().day.at('07:50').do(API.start, 'orders_1mnth', 'terehov', 'Ozon')
    my_scheduler.every().day.at('07:55').do(API.start, 'orders_1week', 'terehov', 'Ozon')
    my_scheduler.every().day.at('08:00').do(API.start, 'orders_2days', 'terehov', 'Ozon')

    # dnk
    my_scheduler.every().day.at('08:05').do(API.start, 'orders_alt', 'dnk', 'Ozon')
    my_scheduler.every().day.at('08:10').do(API.start, 'products', 'dnk', 'Ozon')
    my_scheduler.every().day.at('08:15').do(API.start, 'orders_1mnth', 'dnk', 'Ozon')
    my_scheduler.every().day.at('08:20').do(API.start, 'orders_1week', 'dnk', 'Ozon')
    my_scheduler.every().day.at('08:25').do(API.start, 'orders_2days', 'dnk', 'Ozon')

    # 2ruz
    my_scheduler.every().day.at('08:30').do(API.start, 'orders_alt', '2ruz', 'Ozon')
    my_scheduler.every().day.at('08:35').do(API.start, 'products', '2ruz', 'Ozon')
    my_scheduler.every().day.at('08:40').do(API.start, 'orders_1mnth', '2ruz', 'Ozon')
    my_scheduler.every().day.at('08:45').do(API.start, 'orders_1week', '2ruz', 'Ozon')
    my_scheduler.every().day.at('08:50').do(API.start, 'orders_2days', '2ruz', 'Ozon')

    # peco
    my_scheduler.every().day.at('08:55').do(API.start, 'orders_alt', 'peco', 'Ozon')
    my_scheduler.every().day.at('09:00').do(API.start, 'products', 'peco', 'Ozon')
    my_scheduler.every().day.at('09:05').do(API.start, 'orders_1mnth', 'peco', 'Ozon')
    my_scheduler.every().day.at('09:10').do(API.start, 'orders_1week', 'peco', 'Ozon')
    my_scheduler.every().day.at('09:15').do(API.start, 'orders_2days', 'peco', 'Ozon')

    # peco_bathroom
    my_scheduler.every().day.at('09:20').do(API.start, 'orders_alt', 'peco_bathroom', 'Ozon')
    my_scheduler.every().day.at('09:25').do(API.start, 'products', 'peco_bathroom', 'Ozon')
    my_scheduler.every().day.at('09:30').do(API.start, 'orders_1mnth', 'peco_bathroom', 'Ozon')
    my_scheduler.every().day.at('09:35').do(API.start, 'orders_1week', 'peco_bathroom', 'Ozon')
    my_scheduler.every().day.at('09:40').do(API.start, 'orders_2days', 'peco_bathroom', 'Ozon')

    logging.getLogger("extraInfo").info("Ozon scheduled")

    while True:
        my_scheduler.run_pending()
