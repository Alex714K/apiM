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
    my_scheduler.every().day.at('03:13').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('03:16').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('03:19').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('03:22').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('03:25').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('03:28').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('03:31').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('03:34').do(API.execute, Folder.WB, Client.Grand, NameOfSheet.CardsList)

    # terehov
    my_scheduler.every().day.at('03:37').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('03:40').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('03:43').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('03:46').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('03:49').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('03:52').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('03:55').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('03:58').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('04:01').do(API.execute, Folder.WB, Client.Terehov, NameOfSheet.CardsList)

    # dnk
    my_scheduler.every().day.at('04:04').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('04:07').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('04:10').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('04:13').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('04:16').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('04:19').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('04:22').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('04:25').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('04:28').do(API.execute, Folder.WB, Client.Dnk, NameOfSheet.CardsList)

    # planeta
    my_scheduler.every().day.at('04:31').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('04:34').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('04:37').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('04:40').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('04:43').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('04:46').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('04:49').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('04:52').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('04:55').do(API.execute, Folder.WB, Client.Planeta, NameOfSheet.CardsList)

    # 2ruz
    my_scheduler.every().day.at('04:58').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('05:01').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('05:04').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('05:07').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('05:10').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('05:13').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('05:16').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('05:19').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('05:22').do(API.execute, Folder.WB, Client.TwoRuz, NameOfSheet.CardsList)

    # peco
    my_scheduler.every().day.at('05:25').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('05:28').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('05:31').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('05:34').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('05:37').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('05:40').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('05:43').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('05:46').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('05:49').do(API.execute, Folder.WB, Client.Peco, NameOfSheet.CardsList)

    # rus_house
    my_scheduler.every().day.at('05:52').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('05:55').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('05:58').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('06:01').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('06:04').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('06:07').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('06:10').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('06:13').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('06:16').do(API.execute, Folder.WB, Client.RusHouse, NameOfSheet.CardsList)

    # sisin
    my_scheduler.every().day.at('06:19').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('06:22').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('06:25').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('06:28').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('06:31').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('06:34').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('06:37').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('06:40').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('06:43').do(API.execute, Folder.WB, Client.Sisin, NameOfSheet.CardsList)

    # briovi
    my_scheduler.every().day.at('06:46').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('06:49').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('06:52').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('06:55').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('06:58').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('07:01').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('07:04').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('07:07').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('07:10').do(API.execute, Folder.WB, Client.Briovi, NameOfSheet.CardsList)

    # medavibe
    my_scheduler.every().day.at('07:13').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Orders1Month)
    my_scheduler.every().day.at('07:16').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Orders1Week)
    my_scheduler.every().day.at('07:19').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Orders2Days)
    my_scheduler.every().day.at('07:22').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.Sales1Month)
    my_scheduler.every().day.at('07:25').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.TariffsBoxes)
    my_scheduler.every().day.at('07:28').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.TariffsPallet)
    my_scheduler.every().day.at('07:31').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.ProductsWB)
    my_scheduler.every().day.at('07:34').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.ProductsMP)
    my_scheduler.every().day.at('07:37').do(API.execute, Folder.WB, Client.Medavibe, NameOfSheet.CardsList)

    # Платное хранение
    # my_scheduler.every().day.at('00:00').do(API.execute, 'storage_paid', 'planeta', 'WB')

    logging.getLogger("extraInfo").info("WB scheduled")

    while True:
        try:
            my_scheduler.run_pending()
        except Exception as ex:
            API.logger.warning(f"Smth happend ({ex})")
        time.sleep(1)
