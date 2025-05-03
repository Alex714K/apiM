import logging
import schedule
from plugins.Api import Api


def WB_cycle():
    API = Api()
    my_scheduler = schedule.Scheduler()
    # grand
    my_scheduler.every(30).minutes.do(API.start, 'stocks', 'grand', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', 'grand', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', 'grand', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', 'grand', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'grand', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', 'grand', 'WB')

    # terehov
    my_scheduler.every(30).minutes.do(API.start, 'stocks', 'terehov', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', 'terehov', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', 'terehov', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', 'terehov', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'terehov', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', 'terehov', 'WB')

    # dnk
    my_scheduler.every(30).minutes.do(API.start, 'stocks', 'dnk', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', 'dnk', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', 'dnk', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', 'dnk', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'dnk', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', 'dnk', 'WB')

    # planeta
    my_scheduler.every(30).minutes.do(API.start, 'stocks', 'planeta', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', 'planeta', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', 'planeta', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', 'planeta', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'planeta', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', 'planeta', 'WB')

    # 2ruz
    my_scheduler.every(30).minutes.do(API.start, 'stocks', '2ruz', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', '2ruz', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', '2ruz', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', '2ruz', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', '2ruz', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', '2ruz', 'WB')

    # peco
    my_scheduler.every(30).minutes.do(API.start, 'stocks', 'peco', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', 'peco', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', 'peco', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', 'peco', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'peco', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', 'peco', 'WB')

    # rus_house
    my_scheduler.every(30).minutes.do(API.start, 'stocks', 'rus_house', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', 'rus_house', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', 'rus_house', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', 'rus_house', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'rus_house', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', 'rus_house', 'WB')

    # sisin
    my_scheduler.every(30).minutes.do(API.start, 'stocks', 'sisin', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'stocks_hard', 'sisin', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'orders_today', 'sisin', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'sales_today', 'sisin', 'WB')
    my_scheduler.every(15).minutes.do(API.start, 'prices', 'sisin', 'WB')
    my_scheduler.every(30).minutes.do(API.start, 'coefficients', 'sisin', 'WB')

    # fixed_prices
    my_scheduler.every().hour.at('23:00').do(API.start, 'fixed_prices', 'grand', 'WB')
    my_scheduler.every().hour.at('23:05').do(API.start, 'fixed_prices', 'terehov', 'WB')
    my_scheduler.every().hour.at('23:10').do(API.start, 'fixed_prices', 'dnk', 'WB')
    my_scheduler.every().hour.at('23:15').do(API.start, 'fixed_prices', 'planeta', 'WB')
    my_scheduler.every().hour.at('23:20').do(API.start, 'fixed_prices', '2ruz', 'WB')
    my_scheduler.every().hour.at('23:25').do(API.start, 'fixed_prices', 'peco', 'WB')
    my_scheduler.every().hour.at('23:30').do(API.start, 'fixed_prices', 'rus_house', 'WB')
    my_scheduler.every().hour.at('23:35').do(API.start, 'fixed_prices', 'sisin', 'WB')

    # grand
    my_scheduler.every().day.at('03:10').do(API.start, 'orders_1mnth', 'grand', 'WB')
    my_scheduler.every().day.at('03:15').do(API.start, 'orders_1week', 'grand', 'WB')
    my_scheduler.every().day.at('03:20').do(API.start, 'orders_2days', 'grand', 'WB')
    my_scheduler.every().day.at('03:25').do(API.start, 'sales_1mnth', 'grand', 'WB')
    my_scheduler.every().day.at('03:30').do(API.start, 'tariffs_boxes', 'grand', 'WB')
    my_scheduler.every().day.at('03:35').do(API.start, 'tariffs_pallet', 'grand', 'WB')

    # terehov
    my_scheduler.every().day.at('03:40').do(API.start, 'orders_1mnth', 'terehov', 'WB')
    my_scheduler.every().day.at('03:45').do(API.start, 'orders_1week', 'terehov', 'WB')
    my_scheduler.every().day.at('03:50').do(API.start, 'orders_2days', 'terehov', 'WB')
    my_scheduler.every().day.at('03:55').do(API.start, 'sales_1mnth', 'terehov', 'WB')
    my_scheduler.every().day.at('04:00').do(API.start, 'tariffs_boxes', 'terehov', 'WB')
    my_scheduler.every().day.at('04:05').do(API.start, 'tariffs_pallet', 'terehov', 'WB')

    # dnk
    my_scheduler.every().day.at('04:10').do(API.start, 'orders_1mnth', 'dnk', 'WB')
    my_scheduler.every().day.at('04:15').do(API.start, 'orders_1week', 'dnk', 'WB')
    my_scheduler.every().day.at('04:20').do(API.start, 'orders_2days', 'dnk', 'WB')
    my_scheduler.every().day.at('04:25').do(API.start, 'sales_1mnth', 'dnk', 'WB')
    my_scheduler.every().day.at('04:30').do(API.start, 'tariffs_boxes', 'dnk', 'WB')
    my_scheduler.every().day.at('04:35').do(API.start, 'tariffs_pallet', 'dnk', 'WB')

    # planeta
    my_scheduler.every().day.at('04:40').do(API.start, 'orders_1mnth', 'planeta', 'WB')
    my_scheduler.every().day.at('04:45').do(API.start, 'orders_1week', 'planeta', 'WB')
    my_scheduler.every().day.at('04:50').do(API.start, 'orders_2days', 'planeta', 'WB')
    my_scheduler.every().day.at('04:55').do(API.start, 'sales_1mnth', 'planeta', 'WB')
    my_scheduler.every().day.at('05:00').do(API.start, 'tariffs_boxes', 'planeta', 'WB')
    my_scheduler.every().day.at('05:05').do(API.start, 'tariffs_pallet', 'planeta', 'WB')

    # 2ruz
    my_scheduler.every().day.at('05:10').do(API.start, 'orders_1mnth', '2ruz', 'WB')
    my_scheduler.every().day.at('05:15').do(API.start, 'orders_1week', '2ruz', 'WB')
    my_scheduler.every().day.at('05:20').do(API.start, 'orders_2days', '2ruz', 'WB')
    my_scheduler.every().day.at('05:25').do(API.start, 'sales_1mnth', '2ruz', 'WB')
    my_scheduler.every().day.at('05:30').do(API.start, 'tariffs_boxes', '2ruz', 'WB')
    my_scheduler.every().day.at('05:35').do(API.start, 'tariffs_pallet', '2ruz', 'WB')

    # peco
    my_scheduler.every().day.at('05:40').do(API.start, 'orders_1mnth', 'peco', 'WB')
    my_scheduler.every().day.at('05:45').do(API.start, 'orders_1week', 'peco', 'WB')
    my_scheduler.every().day.at('05:50').do(API.start, 'orders_2days', 'peco', 'WB')
    my_scheduler.every().day.at('05:55').do(API.start, 'sales_1mnth', 'peco', 'WB')
    my_scheduler.every().day.at('06:00').do(API.start, 'tariffs_boxes', 'peco', 'WB')
    my_scheduler.every().day.at('06:05').do(API.start, 'tariffs_pallet', 'peco', 'WB')

    # rus_house
    my_scheduler.every().day.at('06:10').do(API.start, 'orders_1mnth', 'rus_house', 'WB')
    my_scheduler.every().day.at('06:15').do(API.start, 'orders_1week', 'rus_house', 'WB')
    my_scheduler.every().day.at('06:20').do(API.start, 'orders_2days', 'rus_house', 'WB')
    my_scheduler.every().day.at('06:25').do(API.start, 'sales_1mnth', 'rus_house', 'WB')
    my_scheduler.every().day.at('06:30').do(API.start, 'tariffs_boxes', 'rus_house', 'WB')
    my_scheduler.every().day.at('06:35').do(API.start, 'tariffs_pallet', 'rus_house', 'WB')

    # sisin
    my_scheduler.every().day.at('06:40').do(API.start, 'orders_1mnth', 'sisin', 'WB')
    my_scheduler.every().day.at('06:45').do(API.start, 'orders_1week', 'sisin', 'WB')
    my_scheduler.every().day.at('06:50').do(API.start, 'orders_2days', 'sisin', 'WB')
    my_scheduler.every().day.at('06:55').do(API.start, 'sales_1mnth', 'sisin', 'WB')
    my_scheduler.every().day.at('07:00').do(API.start, 'tariffs_boxes', 'sisin', 'WB')
    my_scheduler.every().day.at('07:05').do(API.start, 'tariffs_pallet', 'sisin', 'WB')

    # Платное хранение
    # my_scheduler.every().day.at('00:00').do(API.start, 'storage_paid', 'planeta', 'WB')

    logging.getLogger("extraInfo").info("WB scheduled")

    while True:
        my_scheduler.run_pending()
