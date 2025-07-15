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
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.StockOnWarehouse)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Sendings)

    # terehov
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.StockOnWarehouse)

    # dnk
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.StockOnWarehouse)

    # 2ruz
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.StockOnWarehouse)

    # peco
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.StockOnWarehouse)

    # peco_bathroom
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.StockOnWarehouse)

    # briovi
    my_scheduler.every(15).minutes.do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Prices)
    my_scheduler.every(30).minutes.do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.StockOnWarehouse)

    # grand
    my_scheduler.every().day.at('09:50').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('09:55').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Analytics)
    my_scheduler.every().day.at('10:00').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Products)
    my_scheduler.every().day.at('10:05').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('10:10').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:15').do(API.execute, Folder.Ozon, Client.Grand, NameOfSheet.Orders2Days)

    # terehov
    my_scheduler.every().day.at('10:20').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('10:25').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Products)
    my_scheduler.every().day.at('10:30').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('10:35').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('10:40').do(API.execute, Folder.Ozon, Client.Terehov, NameOfSheet.Orders2Days)

    # dnk
    my_scheduler.every().day.at('10:45').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('10:50').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Products)
    my_scheduler.every().day.at('10:55').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('11:00').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('11:05').do(API.execute, Folder.Ozon, Client.Dnk, NameOfSheet.Orders2Days)

    # 2ruz
    my_scheduler.every().day.at('11:10').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('11:15').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Products)
    my_scheduler.every().day.at('11:20').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('11:25').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('11:30').do(API.execute, Folder.Ozon, Client.TwoRuz, NameOfSheet.Orders2Days)

    # peco
    my_scheduler.every().day.at('11:35').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('11:40').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Products)
    my_scheduler.every().day.at('11:45').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('11:50').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('11:55').do(API.execute, Folder.Ozon, Client.Peco, NameOfSheet.Orders2Days)

    # peco_bathroom
    my_scheduler.every().day.at('12:00').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('12:05').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Products)
    my_scheduler.every().day.at('12:10').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('12:15').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('12:20').do(API.execute, Folder.Ozon, Client.PecoBathroom, NameOfSheet.Orders2Days)

    # briovi
    my_scheduler.every().day.at('12:25').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.OrdersAlt)
    my_scheduler.every().day.at('12:30').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Products)
    my_scheduler.every().day.at('12:35').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('12:40').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('12:45').do(API.execute, Folder.Ozon, Client.Briovi, NameOfSheet.Orders2Days)

    logging.getLogger("extraInfo").info("Ozon scheduled")

    while True:
        try:
            my_scheduler.run_pending()
        except Exception as ex:
            API.logger.warning(f"Smth happend ({ex})")
        time.sleep(1)
