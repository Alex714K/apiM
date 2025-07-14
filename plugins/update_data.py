import datetime


class UpdateAndSchedules:
    names_of_sheet_wb_oneday: list[str] = [
        "orders_1mnth",
        "orders_1week",
        "orders_2days",
        "sales_1mnth",
        "fixed_prices",
        "tariffs_boxes",
        "tariffs_pallet",
        "productsWB",
        "productsMP"
    ]

    names_of_sheet_wb_interval: list[list[str]] = [
        ["stocks", "30"],
        ["stocks_hard", "30"],
        ["orders_today", "30"],
        ["sales_today", "30"],
        ["prices", "15"],
        ["coefficients", "30"],
    ]

    names_of_sheet_ozon_oneday: list[str] = [
        "orders_alt",
        "analytics",
        "products",
        "orders_1mnth",
        "orders_1week",
        "orders_2days",
    ]

    names_of_sheet_ozon_interval: list[list[str]] = [
        ["prices", "15"],
        ["stock_on_warehouses", "30"],
        ["sendings", "30"],
    ]

    start_time = datetime.datetime(2000, 1, 1, hour=3, minute=0, second=0)
    clients_wb_private = [
        "grand",
        "terehov",
        "dnk",
        "planeta",
        "2ruz",
        "peco",
        "rus_house",
        "sisin",
        "briovi",
        "medavibe",
    ]

    clients_wb = list()
    for client in clients_wb_private:
        clients_wb.append((client, datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour,
                                                     start_time.minute, start_time.second)))
        start_time += datetime.timedelta(minutes=5 * len(names_of_sheet_wb_oneday))

    clients_ozon_private = [
        "grand",
        "terehov",
        "dnk",
        "2ruz",
        "peco",
        "peco_bathroom",
        "briovi",
    ]

    clients_ozon = list()
    for client in clients_ozon_private:
        clients_ozon.append((client,
                             datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour,
                                               start_time.minute, start_time.second)))
        start_time += datetime.timedelta(minutes=5 * len(names_of_sheet_ozon_oneday))
