import logging

import schedule
from plugins.Api import Api


def WB_cycle():
    API = Api()
    # grand
    schedule.every(30).minutes.do(API.start, 'stocks', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'grand', 'WB')
    schedule.every(15).minutes.do(API.start, 'prices', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'grand', 'WB')

    # terehov
    schedule.every(30).minutes.do(API.start, 'stocks', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'terehov', 'WB')
    schedule.every(15).minutes.do(API.start, 'prices', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'terehov', 'WB')

    # dnk
    schedule.every(30).minutes.do(API.start, 'stocks', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'dnk', 'WB')
    schedule.every(15).minutes.do(API.start, 'prices', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'dnk', 'WB')

    # planeta
    schedule.every(30).minutes.do(API.start, 'stocks', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'planeta', 'WB')
    schedule.every(15).minutes.do(API.start, 'prices', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'planeta', 'WB')

    # 2ruz
    schedule.every(30).minutes.do(API.start, 'stocks', '2ruz', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', '2ruz', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', '2ruz', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', '2ruz', 'WB')
    schedule.every(15).minutes.do(API.start, 'prices', '2ruz', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', '2ruz', 'WB')

    # peco
    schedule.every(30).minutes.do(API.start, 'stocks', 'peco', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'peco', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'peco', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'peco', 'WB')
    schedule.every(15).minutes.do(API.start, 'prices', 'peco', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'peco', 'WB')

    # rus_house
    schedule.every(30).minutes.do(API.start, 'stocks', 'rus_house', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'rus_house', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'rus_house', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'rus_house', 'WB')
    schedule.every(15).minutes.do(API.start, 'prices', 'rus_house', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'rus_house', 'WB')

    # fixed_prices
    schedule.every().hour.at('23:00').do(API.start, 'fixed_prices', 'grand', 'WB')
    schedule.every().hour.at('23:05').do(API.start, 'fixed_prices', 'terehov', 'WB')
    schedule.every().hour.at('23:10').do(API.start, 'fixed_prices', 'dnk', 'WB')
    schedule.every().hour.at('23:15').do(API.start, 'fixed_prices', 'planeta', 'WB')
    schedule.every().hour.at('23:20').do(API.start, 'fixed_prices', '2ruz', 'WB')
    schedule.every().hour.at('23:25').do(API.start, 'fixed_prices', 'peco', 'WB')
    schedule.every().hour.at('23:30').do(API.start, 'fixed_prices', 'rus_house', 'WB')

    # grand
    schedule.every().day.at('03:10').do(API.start, 'orders_1mnth', 'grand', 'WB')
    schedule.every().day.at('03:15').do(API.start, 'orders_1week', 'grand', 'WB')
    schedule.every().day.at('03:20').do(API.start, 'orders_2days', 'grand', 'WB')
    schedule.every().day.at('03:25').do(API.start, 'sales_1mnth', 'grand', 'WB')
    schedule.every().day.at('03:30').do(API.start, 'tariffs_boxes', 'grand', 'WB')
    schedule.every().day.at('03:35').do(API.start, 'tariffs_pallet', 'grand', 'WB')

    # terehov
    schedule.every().day.at('03:40').do(API.start, 'orders_1mnth', 'terehov', 'WB')
    schedule.every().day.at('03:45').do(API.start, 'orders_1week', 'terehov', 'WB')
    schedule.every().day.at('03:50').do(API.start, 'orders_2days', 'terehov', 'WB')
    schedule.every().day.at('03:55').do(API.start, 'sales_1mnth', 'terehov', 'WB')
    schedule.every().day.at('04:00').do(API.start, 'tariffs_boxes', 'terehov', 'WB')
    schedule.every().day.at('04:05').do(API.start, 'tariffs_pallet', 'terehov', 'WB')

    # dnk
    schedule.every().day.at('04:10').do(API.start, 'orders_1mnth', 'dnk', 'WB')
    schedule.every().day.at('04:15').do(API.start, 'orders_1week', 'dnk', 'WB')
    schedule.every().day.at('04:20').do(API.start, 'orders_2days', 'dnk', 'WB')
    schedule.every().day.at('04:25').do(API.start, 'sales_1mnth', 'dnk', 'WB')
    schedule.every().day.at('04:30').do(API.start, 'tariffs_boxes', 'dnk', 'WB')
    schedule.every().day.at('04:35').do(API.start, 'tariffs_pallet', 'dnk', 'WB')

    # planeta
    schedule.every().day.at('04:40').do(API.start, 'orders_1mnth', 'planeta', 'WB')
    schedule.every().day.at('04:45').do(API.start, 'orders_1week', 'planeta', 'WB')
    schedule.every().day.at('04:50').do(API.start, 'orders_2days', 'planeta', 'WB')
    schedule.every().day.at('04:55').do(API.start, 'sales_1mnth', 'planeta', 'WB')
    schedule.every().day.at('05:00').do(API.start, 'tariffs_boxes', 'planeta', 'WB')
    schedule.every().day.at('05:05').do(API.start, 'tariffs_pallet', 'planeta', 'WB')

    # 2ruz
    schedule.every().day.at('05:10').do(API.start, 'orders_1mnth', '2ruz', 'WB')
    schedule.every().day.at('05:15').do(API.start, 'orders_1week', '2ruz', 'WB')
    schedule.every().day.at('05:20').do(API.start, 'orders_2days', '2ruz', 'WB')
    schedule.every().day.at('05:25').do(API.start, 'sales_1mnth', '2ruz', 'WB')
    schedule.every().day.at('05:30').do(API.start, 'tariffs_boxes', '2ruz', 'WB')
    schedule.every().day.at('05:35').do(API.start, 'tariffs_pallet', '2ruz', 'WB')

    # peco
    schedule.every().day.at('05:40').do(API.start, 'orders_1mnth', 'peco', 'WB')
    schedule.every().day.at('05:45').do(API.start, 'orders_1week', 'peco', 'WB')
    schedule.every().day.at('05:50').do(API.start, 'orders_2days', 'peco', 'WB')
    schedule.every().day.at('05:55').do(API.start, 'sales_1mnth', 'peco', 'WB')
    schedule.every().day.at('06:00').do(API.start, 'tariffs_boxes', 'peco', 'WB')
    schedule.every().day.at('06:05').do(API.start, 'tariffs_pallet', 'peco', 'WB')

    # rus_house
    schedule.every().day.at('06:10').do(API.start, 'orders_1mnth', 'rus_house', 'WB')
    schedule.every().day.at('06:15').do(API.start, 'orders_1week', 'rus_house', 'WB')
    schedule.every().day.at('06:20').do(API.start, 'orders_2days', 'rus_house', 'WB')
    schedule.every().day.at('06:25').do(API.start, 'sales_1mnth', 'rus_house', 'WB')
    schedule.every().day.at('06:30').do(API.start, 'tariffs_boxes', 'rus_house', 'WB')
    schedule.every().day.at('06:35').do(API.start, 'tariffs_pallet', 'rus_house', 'WB')

    # Платное хранение
    # schedule.every().day.at('00:00').do(API.start, 'storage_paid', 'planeta', 'WB')

    logging.getLogger("extraInfo").info("WB scheduled")
