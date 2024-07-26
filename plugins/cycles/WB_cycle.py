import schedule
from plugins.Api import Api
from plugins.Logger.Logger import getLogger


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

    # Финансовые отчёты
    schedule.every().day.at("02:00").do(API.start, 'statements', 'planeta', 'WB')
    schedule.every().day.at("17:00").do(API.start, 'statements', 'planeta', 'WB')

    # Утро гранд
    schedule.every().day.at("01:30").do(API.start, 'stocks', 'grand', 'WB')
    schedule.every().day.at("01:35").do(API.start, 'orders_1mnth', 'grand', 'WB')
    schedule.every().day.at("01:40").do(API.start, 'orders_1week', 'grand', 'WB')
    schedule.every().day.at("01:45").do(API.start, 'orders_2days', 'grand', 'WB')
    schedule.every().day.at("01:50").do(API.start, 'orders_today', 'grand', 'WB')
    schedule.every().day.at("01:55").do(API.start, 'tariffs_boxes', 'grand', 'WB')
    schedule.every().day.at("02:00").do(API.start, 'tariffs_pallet', 'grand', 'WB')

    # День гранд
    schedule.every().day.at("13:30").do(API.start, 'stocks', 'grand', 'WB')
    schedule.every().day.at("13:35").do(API.start, 'orders_1mnth', 'grand', 'WB')
    schedule.every().day.at("13:40").do(API.start, 'orders_1week', 'grand', 'WB')
    schedule.every().day.at("13:45").do(API.start, 'orders_2days', 'grand', 'WB')
    schedule.every().day.at("13:50").do(API.start, 'orders_today', 'grand', 'WB')
    schedule.every().day.at("13:55").do(API.start, 'tariffs_boxes', 'grand', 'WB')
    schedule.every().day.at("14:00").do(API.start, 'tariffs_pallet', 'grand', 'WB')

    # Утро терехов
    schedule.every().day.at("02:05").do(API.start, 'stocks', 'terehov', 'WB')
    schedule.every().day.at("02:10").do(API.start, 'orders_1mnth', 'terehov', 'WB')
    schedule.every().day.at("02:15").do(API.start, 'orders_1week', 'terehov', 'WB')
    schedule.every().day.at("02:20").do(API.start, 'orders_2days', 'terehov', 'WB')
    schedule.every().day.at("02:25").do(API.start, 'orders_today', 'terehov', 'WB')
    schedule.every().day.at("02:30").do(API.start, 'tariffs_boxes', 'terehov', 'WB')
    schedule.every().day.at("02:35").do(API.start, 'tariffs_pallet', 'terehov', 'WB')

    # День терехов
    schedule.every().day.at("14:05").do(API.start, 'stocks', 'terehov', 'WB')
    schedule.every().day.at("14:10").do(API.start, 'orders_1mnth', 'terehov', 'WB')
    schedule.every().day.at("14:15").do(API.start, 'orders_1week', 'terehov', 'WB')
    schedule.every().day.at("14:20").do(API.start, 'orders_2days', 'terehov', 'WB')
    schedule.every().day.at("14:25").do(API.start, 'orders_today', 'terehov', 'WB')
    schedule.every().day.at("14:30").do(API.start, 'tariffs_boxes', 'terehov', 'WB')
    schedule.every().day.at("14:35").do(API.start, 'tariffs_pallet', 'terehov', 'WB')

    # Утро днк
    schedule.every().day.at("02:40").do(API.start, 'stocks', 'dnk', 'WB')
    schedule.every().day.at("02:45").do(API.start, 'orders_1mnth', 'dnk', 'WB')
    schedule.every().day.at("02:50").do(API.start, 'orders_1week', 'dnk', 'WB')
    schedule.every().day.at("02:55").do(API.start, 'orders_2days', 'dnk', 'WB')
    schedule.every().day.at("03:00").do(API.start, 'orders_today', 'dnk', 'WB')
    schedule.every().day.at("03:05").do(API.start, 'tariffs_boxes', 'dnk', 'WB')
    schedule.every().day.at("03:10").do(API.start, 'tariffs_pallet', 'dnk', 'WB')

    # День днк
    schedule.every().day.at("14:45").do(API.start, 'orders_1mnth', 'dnk', 'WB')
    schedule.every().day.at("14:50").do(API.start, 'orders_1week', 'dnk', 'WB')
    schedule.every().day.at("14:55").do(API.start, 'orders_2days', 'dnk', 'WB')
    schedule.every().day.at("15:00").do(API.start, 'orders_today', 'dnk', 'WB')
    schedule.every().day.at("15:05").do(API.start, 'tariffs_boxes', 'dnk', 'WB')
    schedule.every().day.at("15:10").do(API.start, 'tariffs_pallet', 'dnk', 'WB')

    # Утро планета
    schedule.every().day.at("03:15").do(API.start, 'stocks', 'planeta', 'WB')
    schedule.every().day.at("03:20").do(API.start, 'orders_1mnth', 'planeta', 'WB')
    schedule.every().day.at("03:25").do(API.start, 'orders_1week', 'planeta', 'WB')
    schedule.every().day.at("03:30").do(API.start, 'orders_2days', 'planeta', 'WB')
    schedule.every().day.at("03:35").do(API.start, 'orders_today', 'planeta', 'WB')
    schedule.every().day.at("03:40").do(API.start, 'tariffs_boxes', 'planeta', 'WB')
    schedule.every().day.at("03:45").do(API.start, 'tariffs_pallet', 'planeta', 'WB')

    # День планета
    schedule.every().day.at("15:15").do(API.start, 'stocks', 'planeta', 'WB')
    schedule.every().day.at("15:20").do(API.start, 'orders_1mnth', 'planeta', 'WB')
    schedule.every().day.at("15:25").do(API.start, 'orders_1week', 'planeta', 'WB')
    schedule.every().day.at("15:30").do(API.start, 'orders_2days', 'planeta', 'WB')
    schedule.every().day.at("15:35").do(API.start, 'orders_today', 'planeta', 'WB')
    schedule.every().day.at("15:40").do(API.start, 'tariffs_boxes', 'planeta', 'WB')
    schedule.every().day.at("15:45").do(API.start, 'tariffs_pallet', 'planeta', 'WB')

    # Платное хранение
    # schedule.every().day.at('00:00').do(API.start, 'storage_paid', 'planeta', 'WB')

    getLogger("extraInfo").info("WB scheduled")
