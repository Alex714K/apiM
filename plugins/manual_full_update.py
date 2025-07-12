from plugins.Api import Api
from plugins.update_data import UpdateAndSchedules


def manual_full_update(API: Api):
    # print("Started WB")
    # print("-" * 25)

    for client, time in UpdateAndSchedules.clients_wb:
        # print(f"client: {client}")
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_wb_oneday:
            if name_of_sheet == "orders_1mnth" and client == "grand":
                continue
            API.start(name_of_sheet, client, "WB")
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_wb_interval:
            # if name_of_sheet == ["stocks_hard", "30"] and client != "grand":
            #     continue
            API.start(name_of_sheet[0], client, "WB")

    # print("-" * 25)
    # print("Started Ozon")
    # print("-" * 25)

    for client, time in UpdateAndSchedules.clients_ozon:
        # print(f"client: {client}")
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_ozon_oneday:
            if client != "grand" and (name_of_sheet == "sendings" or name_of_sheet == "analytics"):
                continue
            API.start(name_of_sheet, client, "Ozon")
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_ozon_interval:
            if client != "grand" and (name_of_sheet[0] == "sendings" or name_of_sheet[0] == "analytics"):
                continue
            API.start(name_of_sheet[0], client, "Ozon")
