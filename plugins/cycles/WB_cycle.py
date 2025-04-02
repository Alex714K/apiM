import logging

import schedule
from plugins.Api import Api


def WB_cycle():
    API = Api()
    # Цены
    schedule.every(10).minutes.do(API.start, 'prices', 'grand', 'WB')
    schedule.every().day.at("23:00").do(API.start, 'fixed_prices', 'grand', 'WB')

    schedule.every(10).minutes.do(API.start, 'prices', 'terehov', 'WB')
    schedule.every().day.at("23:05").do(API.start, 'fixed_prices', 'terehov', 'WB')

    schedule.every(10).minutes.do(API.start, 'prices', 'dnk', 'WB')
    schedule.every().day.at("23:10").do(API.start, 'fixed_prices', 'dnk', 'WB')

    schedule.every(10).minutes.do(API.start, 'prices', 'planeta', 'WB')
    schedule.every().day.at("23:15").do(API.start, 'fixed_prices', 'planeta', 'WB')

    schedule.every(10).minutes.do(API.start, 'prices', '2ruz', 'WB')
    schedule.every().day.at("23:15").do(API.start, 'fixed_prices', '2ruz', 'WB')

    # Статистика приёмки
    schedule.every(30).minutes.do(API.start, 'coefficients', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'coefficients', '2ruz', 'WB')

    # Финансовые отчёты
    # schedule.every().day.at("02:12").do(API.start, 'statements', 'planeta', 'WB')
    # schedule.every().day.at("17:00").do(API.start, 'statements', 'planeta', 'WB')

    # Заказы за сегодня
    schedule.every(30).minutes.do(API.start, 'orders_today', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'orders_today', '2ruz', 'WB')

    # Продаже за сегодня
    schedule.every(30).minutes.do(API.start, 'sales_today', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'sales_today', '2ruz', 'WB')

    # Продаже за месяц
    schedule.every().hour.do(API.start, 'sales_today', 'grand', 'WB')
    schedule.every().hour.do(API.start, 'sales_today', 'terehov', 'WB')
    schedule.every().hour.do(API.start, 'sales_today', 'dnk', 'WB')
    schedule.every().hour.do(API.start, 'sales_today', 'planeta', 'WB')
    schedule.every().hour.do(API.start, 'sales_today', '2ruz', 'WB')

    # Остатки
    schedule.every(30).minutes.do(API.start, 'stocks', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks', '2ruz', 'WB')

    # Остатки новые
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'grand', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'terehov', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'dnk', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', 'planeta', 'WB')
    schedule.every(30).minutes.do(API.start, 'stocks_hard', '2ruz', 'WB')
    # Утро 2ruz
    schedule.every().day.at("23:45").do(API.start, 'orders_1mnth', '2ruz', 'WB')
    schedule.every().day.at("23:50").do(API.start, 'orders_1week', '2ruz', 'WB')
    schedule.every().day.at("23:55").do(API.start, 'orders_2days', '2ruz', 'WB')
    schedule.every().day.at("00:00").do(API.start, 'tariffs_boxes', '2ruz', 'WB')
    schedule.every().day.at("00:05").do(API.start, 'tariffs_pallet', '2ruz', 'WB')

    # День 2ruz
    schedule.every().day.at("05:45").do(API.start, 'orders_1mnth', '2ruz', 'WB')
    schedule.every().day.at("05:50").do(API.start, 'orders_1week', '2ruz', 'WB')
    schedule.every().day.at("05:55").do(API.start, 'orders_2days', '2ruz', 'WB')
    schedule.every().day.at("06:00").do(API.start, 'tariffs_boxes', '2ruz', 'WB')
    schedule.every().day.at("06:05").do(API.start, 'tariffs_pallet', '2ruz', 'WB')

    # Утро гранд
    schedule.every().day.at("00:10").do(API.start, 'orders_1mnth', 'grand', 'WB')
    schedule.every().day.at("00:15").do(API.start, 'orders_1week', 'grand', 'WB')
    schedule.every().day.at("00:20").do(API.start, 'orders_2days', 'grand', 'WB')
    schedule.every().day.at("00:30").do(API.start, 'tariffs_boxes', 'grand', 'WB')
    schedule.every().day.at("00:35").do(API.start, 'tariffs_pallet', 'grand', 'WB')

    # День гранд
    schedule.every().day.at("06:10").do(API.start, 'orders_1mnth', 'grand', 'WB')
    schedule.every().day.at("06:15").do(API.start, 'orders_1week', 'grand', 'WB')
    schedule.every().day.at("06:20").do(API.start, 'orders_2days', 'grand', 'WB')
    schedule.every().day.at("06:30").do(API.start, 'tariffs_boxes', 'grand', 'WB')
    schedule.every().day.at("06:35").do(API.start, 'tariffs_pallet', 'grand', 'WB')

    # Утро терехов
    schedule.every().day.at("00:45").do(API.start, 'orders_1mnth', 'terehov', 'WB')
    schedule.every().day.at("00:50").do(API.start, 'orders_1week', 'terehov', 'WB')
    schedule.every().day.at("00:55").do(API.start, 'orders_2days', 'terehov', 'WB')
    schedule.every().day.at("01:05").do(API.start, 'tariffs_boxes', 'terehov', 'WB')
    schedule.every().day.at("01:10").do(API.start, 'tariffs_pallet', 'terehov', 'WB')

    # День терехов
    schedule.every().day.at("06:45").do(API.start, 'orders_1mnth', 'terehov', 'WB')
    schedule.every().day.at("06:50").do(API.start, 'orders_1week', 'terehov', 'WB')
    schedule.every().day.at("06:55").do(API.start, 'orders_2days', 'terehov', 'WB')
    schedule.every().day.at("07:05").do(API.start, 'tariffs_boxes', 'terehov', 'WB')
    schedule.every().day.at("07:10").do(API.start, 'tariffs_pallet', 'terehov', 'WB')

    # Утро днк
    schedule.every().day.at("01:20").do(API.start, 'orders_1mnth', 'dnk', 'WB')
    schedule.every().day.at("01:25").do(API.start, 'orders_1week', 'dnk', 'WB')
    schedule.every().day.at("01:30").do(API.start, 'orders_2days', 'dnk', 'WB')
    schedule.every().day.at("01:40").do(API.start, 'tariffs_boxes', 'dnk', 'WB')
    schedule.every().day.at("01:45").do(API.start, 'tariffs_pallet', 'dnk', 'WB')

    # День днк
    schedule.every().day.at("07:15").do(API.start, 'orders_1mnth', 'dnk', 'WB')
    schedule.every().day.at("07:20").do(API.start, 'orders_1week', 'dnk', 'WB')
    schedule.every().day.at("07:25").do(API.start, 'orders_2days', 'dnk', 'WB')
    schedule.every().day.at("07:35").do(API.start, 'tariffs_boxes', 'dnk', 'WB')
    schedule.every().day.at("07:40").do(API.start, 'tariffs_pallet', 'dnk', 'WB')

    # Утро планета
    schedule.every().day.at("01:55").do(API.start, 'orders_1mnth', 'planeta', 'WB')
    schedule.every().day.at("02:00").do(API.start, 'orders_1week', 'planeta', 'WB')
    schedule.every().day.at("02:05").do(API.start, 'orders_2days', 'planeta', 'WB')
    schedule.every().day.at("02:15").do(API.start, 'tariffs_boxes', 'planeta', 'WB')
    schedule.every().day.at("02:20").do(API.start, 'tariffs_pallet', 'planeta', 'WB')

    # День планета
    schedule.every().day.at("07:50").do(API.start, 'orders_1mnth', 'planeta', 'WB')
    schedule.every().day.at("07:55").do(API.start, 'orders_1week', 'planeta', 'WB')
    schedule.every().day.at("08:00").do(API.start, 'orders_2days', 'planeta', 'WB')
    schedule.every().day.at("08:10").do(API.start, 'tariffs_boxes', 'planeta', 'WB')
    schedule.every().day.at("08:15").do(API.start, 'tariffs_pallet', 'planeta', 'WB')

    # Платное хранение
    # schedule.every().day.at('00:00').do(API.start, 'storage_paid', 'planeta', 'WB')

    logging.getLogger("extraInfo").info("WB scheduled")
