import logging
import time
from threading import Thread

import schedule

from plugins.Api import Api
from plugins.navigation.ClientEnum import Client
from plugins.navigation.FolderEnum import Folder
from plugins.navigation.NameOfSheetEnum import NameOfSheet


def ozon_cycle():
    API = Api()
    my_scheduler = schedule.Scheduler()
    # grand
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.StockOnWarehouses)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Sendings)

    # terehov
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.StockOnWarehouses)

    # dnk
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.StockOnWarehouses)

    # 2ruz
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.StockOnWarehouses)

    # peco
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.StockOnWarehouses)

    # peco_bathroom
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.StockOnWarehouses)

    # briovi
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.StockOnWarehouses)

    # grand
    my_scheduler.every().day.at('08:34').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('08:37').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Products)
    my_scheduler.every().day.at('08:40').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('08:43').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('08:46').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Orders2Days)

    # terehov
    my_scheduler.every().day.at('08:49').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('08:52').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Products)
    my_scheduler.every().day.at('08:55').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('08:58').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('09:01').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Orders2Days)

    # dnk
    my_scheduler.every().day.at('09:04').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('09:07').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Products)
    my_scheduler.every().day.at('09:10').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('09:13').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('09:16').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Orders2Days)

    # 2ruz
    my_scheduler.every().day.at('09:19').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('09:22').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Products)
    my_scheduler.every().day.at('09:25').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('09:28').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('09:31').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders2Days)

    # peco
    my_scheduler.every().day.at('09:34').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('09:37').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Products)
    my_scheduler.every().day.at('09:40').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('09:43').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('09:46').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Orders2Days)

    # peco_bathroom
    my_scheduler.every().day.at('09:49').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('09:52').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Products)
    my_scheduler.every().day.at('09:55').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('09:58').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:01').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Orders2Days)

    # briovi
    my_scheduler.every().day.at('10:04').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('10:07').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Products)
    my_scheduler.every().day.at('10:10').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('10:13').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:16').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Orders2Days)

    logging.getLogger("extraInfo").info("Ozon scheduled")

    while True:
        try:
            my_scheduler.run_pending()
        except Exception as ex:
            API.logger.warning(f"Smth happend ({ex})")
        time.sleep(1)
