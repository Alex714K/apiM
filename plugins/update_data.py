import datetime

from plugins.navigation.ClientEnum import Client
from plugins.navigation.NameOfSheetEnum import NameOfSheet


class UpdateAndSchedules:
    names_of_sheet_wb_oneday: list[NameOfSheet] = [
        NameOfSheet.Orders1Month,
        NameOfSheet.Orders1Week,
        NameOfSheet.Orders2Days,
        NameOfSheet.Sales1Month,
        NameOfSheet.FixedPrices,
        NameOfSheet.TariffsBoxes,
        NameOfSheet.TariffsPallet,
        NameOfSheet.ProductsWB,
        NameOfSheet.ProductsMP,
        NameOfSheet.CardsList
    ]

    names_of_sheet_wb_interval: list[list] = [
        [NameOfSheet.Stocks, "30"],
        [NameOfSheet.StocksHard, "30"],
        [NameOfSheet.OrdersToday, "30"],
        [NameOfSheet.SalesToday, "30"],
        [NameOfSheet.SalesToday, "15"],
        [NameOfSheet.Coefficients, "30"],
    ]

    names_of_sheet_ozon_oneday: list[NameOfSheet] = [
        NameOfSheet.OrdersAlt,
        # NameOfSheet.Analytics,
        NameOfSheet.Products,
        NameOfSheet.Orders1Month,
        NameOfSheet.Orders1Week,
        NameOfSheet.Orders2Days,
    ]

    names_of_sheet_ozon_interval: list[list] = [
        [NameOfSheet.Prices, "15"],
        [NameOfSheet.StockOnWarehouses, "30"],
        [NameOfSheet.Sendings, "30"],
    ]

    current_time = datetime.datetime(2000, 1, 1, hour=3, minute=10, second=0)
    start_time = datetime.datetime(2000, 1, 1, hour=3, minute=0, second=0)
    clients_wb_private = [
        Client.Grand,
        Client.Terehov,
        Client.Dnk,
        Client.Planeta,
        Client.TwoRuz,
        Client.Peco,
        Client.RusHouse,
        Client.Sisin,
        Client.Briovi,
        Client.Medavibe,
        Client.DaryAndLove,
        Client.LiaNika
    ]

    clients_wb = list()
    for client in clients_wb_private:
        clients_wb.append((client, datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour,
                                                     start_time.minute, start_time.second)))
        start_time += datetime.timedelta(minutes=5 * len(names_of_sheet_wb_oneday))

    clients_ozon_private = [
        Client.Grand,
        Client.Terehov,
        Client.Dnk,
        Client.TwoRuz,
        Client.Peco,
        Client.PecoBathroom,
        Client.Briovi,
    ]

    clients_ozon = list()
    for client in clients_ozon_private:
        clients_ozon.append((client,
                             datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour,
                                               start_time.minute, start_time.second)))
        start_time += datetime.timedelta(minutes=5 * len(names_of_sheet_ozon_oneday))
