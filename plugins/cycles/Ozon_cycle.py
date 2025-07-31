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
    my_scheduler.every(60).minutes.do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.StockOnWarehouses)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.Sendings)

    # terehov
    my_scheduler.every(60).minutes.do(API.create_thread, Folder.Ozon, Client.Terehov, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.Terehov, NameOfSheet.StockOnWarehouses)

    # dnk
    my_scheduler.every(60).minutes.do(API.create_thread, Folder.Ozon, Client.Dnk, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.Dnk, NameOfSheet.StockOnWarehouses)

    # 2ruz
    my_scheduler.every(60).minutes.do(API.create_thread, Folder.Ozon, Client.TwoRuz, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.TwoRuz, NameOfSheet.StockOnWarehouses)

    # peco
    my_scheduler.every(60).minutes.do(API.create_thread, Folder.Ozon, Client.Peco, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.Peco, NameOfSheet.StockOnWarehouses)

    # peco_bathroom
    my_scheduler.every(60).minutes.do(API.create_thread, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.PecoBathroom,
                                      NameOfSheet.StockOnWarehouses)

    # briovi
    my_scheduler.every(60).minutes.do(API.create_thread, Folder.Ozon, Client.Briovi, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.create_thread, Folder.Ozon, Client.Briovi, NameOfSheet.StockOnWarehouses)

    # grand
    my_scheduler.every().day.at('09:46').do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('09:49').do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.Products)
    my_scheduler.every().day.at('09:52').do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('09:55').do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('09:58').do(API.create_thread, Folder.Ozon, Client.Grand, NameOfSheet.Orders2Days)

    # terehov
    my_scheduler.every().day.at('10:01').do(API.create_thread, Folder.Ozon, Client.Terehov, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('10:04').do(API.create_thread, Folder.Ozon, Client.Terehov, NameOfSheet.Products)
    my_scheduler.every().day.at('10:07').do(API.create_thread, Folder.Ozon, Client.Terehov, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('10:10').do(API.create_thread, Folder.Ozon, Client.Terehov, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:13').do(API.create_thread, Folder.Ozon, Client.Terehov, NameOfSheet.Orders2Days)

    # dnk
    my_scheduler.every().day.at('10:16').do(API.create_thread, Folder.Ozon, Client.Dnk, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('10:19').do(API.create_thread, Folder.Ozon, Client.Dnk, NameOfSheet.Products)
    my_scheduler.every().day.at('10:22').do(API.create_thread, Folder.Ozon, Client.Dnk, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('10:25').do(API.create_thread, Folder.Ozon, Client.Dnk, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:28').do(API.create_thread, Folder.Ozon, Client.Dnk, NameOfSheet.Orders2Days)

    # 2ruz
    my_scheduler.every().day.at('10:31').do(API.create_thread, Folder.Ozon, Client.TwoRuz, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('10:34').do(API.create_thread, Folder.Ozon, Client.TwoRuz, NameOfSheet.Products)
    my_scheduler.every().day.at('10:37').do(API.create_thread, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('10:40').do(API.create_thread, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:43').do(API.create_thread, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders2Days)

    # peco
    my_scheduler.every().day.at('10:46').do(API.create_thread, Folder.Ozon, Client.Peco, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('10:49').do(API.create_thread, Folder.Ozon, Client.Peco, NameOfSheet.Products)
    my_scheduler.every().day.at('10:52').do(API.create_thread, Folder.Ozon, Client.Peco, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('10:55').do(API.create_thread, Folder.Ozon, Client.Peco, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:58').do(API.create_thread, Folder.Ozon, Client.Peco, NameOfSheet.Orders2Days)

    # peco_bathroom
    my_scheduler.every().day.at('11:01').do(API.create_thread, Folder.Ozon, Client.PecoBathroom, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('11:04').do(API.create_thread, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Products)
    my_scheduler.every().day.at('11:07').do(API.create_thread, Folder.Ozon, Client.PecoBathroom,
                                            NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('11:10').do(API.create_thread, Folder.Ozon, Client.PecoBathroom,
                                            NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('11:13').do(API.create_thread, Folder.Ozon, Client.PecoBathroom,
                                            NameOfSheet.Orders2Days)

    # briovi
    my_scheduler.every().day.at('11:16').do(API.create_thread, Folder.Ozon, Client.Briovi, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('11:19').do(API.create_thread, Folder.Ozon, Client.Briovi, NameOfSheet.Products)
    my_scheduler.every().day.at('11:22').do(API.create_thread, Folder.Ozon, Client.Briovi, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('11:25').do(API.create_thread, Folder.Ozon, Client.Briovi, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('11:28').do(API.create_thread, Folder.Ozon, Client.Briovi, NameOfSheet.Orders2Days)

    logging.getLogger("extraInfo").info("Ozon scheduled")

    while True:
        try:
            my_scheduler.run_pending()
        except Exception as ex:
            API.logger.warning(f"Smth happend ({ex})")
        time.sleep(1)
