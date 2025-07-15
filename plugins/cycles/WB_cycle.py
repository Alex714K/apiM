import logging
import time
from threading import Thread

import schedule

from plugins.Api import Api
from plugins.navigation.ClientEnum import Client
from plugins.navigation.FolderEnum import Folder
from plugins.navigation.NameOfSheetEnum import NameOfSheet


def wb_cycle():
    API = Api()
    my_scheduler = schedule.Scheduler()
    # grand
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Grand, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Grand, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Grand, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Grand, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Coefficients)

    # terehov
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Coefficients)

    # dnk
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Coefficients)

    # planeta
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Coefficients)

    # 2ruz
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Coefficients)

    # peco
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Peco, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Peco, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Peco, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Peco, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Coefficients)

    # rus_house
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Coefficients)

    # sisin
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Coefficients)

    # briovi
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Coefficients)

    # medavibe
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Stocks)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.StocksHard)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.OrdersToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.SalesToday)
    my_scheduler.every(15).minutes.do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.SalesToday)
    my_scheduler.every(30).minutes.do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Coefficients)

    # fixed_prices
    my_scheduler.every().day.at('23:00').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:05').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:10').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:15').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:20').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:25').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:30').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:35').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:40').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.FixedPrices)
    my_scheduler.every().day.at('23:45').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.FixedPrices)

    # grand
    my_scheduler.every().day.at('03:10').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('03:15').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('03:20').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('03:25').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('03:30').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('03:35').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('03:40').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('03:45').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.ProductsMP)

    # terehov
    my_scheduler.every().day.at('03:50').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('03:55').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('04:00').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('04:05').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('04:10').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('04:15').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('04:20').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('04:25').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.ProductsMP)

    # dnk
    my_scheduler.every().day.at('04:30').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('04:35').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('04:40').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('04:45').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('04:50').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('04:55').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('05:00').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('05:05').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.ProductsMP)

    # planeta
    my_scheduler.every().day.at('05:10').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('05:15').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('05:20').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('05:25').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('05:30').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('05:35').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('05:40').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('05:45').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.ProductsMP)

    # 2ruz
    my_scheduler.every().day.at('05:50').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('05:55').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('06:00').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('06:05').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('06:10').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('06:15').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('06:20').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('06:25').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.ProductsMP)

    # peco
    my_scheduler.every().day.at('06:30').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('06:35').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('06:40').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('06:45').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('06:50').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('06:55').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('07:00').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('07:05').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.ProductsMP)

    # rus_house
    my_scheduler.every().day.at('07:10').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('07:15').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('07:20').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('07:25').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('07:30').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('07:35').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('07:40').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('07:45').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.ProductsMP)

    # sisin
    my_scheduler.every().day.at('07:50').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('07:55').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('08:00').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('08:05').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('08:10').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('08:15').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('08:20').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('08:25').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.ProductsMP)

    # briovi
    my_scheduler.every().day.at('08:30').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('08:35').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('08:40').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('08:45').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('08:50').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('08:55').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('09:00').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('09:05').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.ProductsMP)

    # medavibe
    my_scheduler.every().day.at('09:10').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('09:15').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('09:20').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('09:25').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('09:30').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('09:35').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('09:40').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('09:45').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.ProductsMP)

    # Платное хранение
    # my_scheduler.every().day.at('00:00').do(API.execute, 'storage_paid', 'planeta', 'WB')

    logging.getLogger("extraInfo").info("WB scheduled")

    while True:
        try:
            my_scheduler.run_pending()
        except Exception as ex:
            API.logger.warning(f"Smth happend ({ex})")
        time.sleep(1)
