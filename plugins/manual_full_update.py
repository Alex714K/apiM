from plugins.Api import Api
from plugins.navigation.ClientEnum import Client
from plugins.navigation.FolderEnum import Folder
from plugins.navigation.NameOfSheetEnum import NameOfSheet
from plugins.update_data import UpdateAndSchedules
import time as sleep_time


def manual_full_update(API_WB: Api, API_OZON: Api):
    # print("Started WB")
    # print("-" * 25)

    for client, time in UpdateAndSchedules.clients_wb:
        sleep_time.sleep(1)
        # print(f"client: {client}")
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_wb_oneday:
            API_WB.create_thread(Folder.WB, client, name_of_sheet)
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_wb_interval:
            # if name_of_sheet == ["stocks_hard", "30"] and client != "grand":
            #     continue
            API_WB.create_thread(Folder.WB, client, name_of_sheet[0])

    # print("-" * 25)
    # print("Started Ozon")
    # print("-" * 25)

    for client, time in UpdateAndSchedules.clients_ozon:
        sleep_time.sleep(1)
        # print(f"client: {client}")
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_ozon_oneday:
            if client != Client.Grand and (name_of_sheet[0] == NameOfSheet.Sendings or name_of_sheet[0] == NameOfSheet.Analytics):
                continue
            API_OZON.create_thread(Folder.Ozon, client, name_of_sheet)
        for name_of_sheet in UpdateAndSchedules.names_of_sheet_ozon_interval:
            if client != Client.Grand and (name_of_sheet[0] == NameOfSheet.Sendings or name_of_sheet[0] == NameOfSheet.Analytics):
                continue
            API_OZON.create_thread(Folder.Ozon, client, name_of_sheet[0])
