import json
import sys
import numpy
import datetime

from plugins.navigation.NameOfSheetEnum import NameOfSheet


class Converter:
    def convert_to_list(self,
                        file: list | dict, name_of_sheet: str) -> (tuple[list, int, list | None] | str):
        """Конвертирует json-объект в список, который подходит для добавления данных из файла в Google Excel"""
        match file:
            case None:
                return 'is None'
            case []:
                return 'is empty'
        if type(file) is not list and type(file) is not dict:
            sys.exit(str(file))

        if name_of_sheet in ['orders_today', 'sales_today', 'stocks', 'rk', 'storage_paid']:
            return self.list_with_dict(file=file)
        elif name_of_sheet == "productsWB" or name_of_sheet == "productsMP":
            return self.products(file=file)
        elif name_of_sheet == "coefficients":
            return self.list_with_dict_without_numpy(file=file)
        elif name_of_sheet in ['orders_1mnth', 'orders_1week', 'orders_2days']:
            return self.orders_not_today(file=file)
        elif name_of_sheet == "sales_1mnth":
            return self.sales_not_today(file=file)
        elif name_of_sheet in ['prices', 'fixed_prices']:
            return self.prices(file=file)
        elif name_of_sheet in ['tariffs_boxes', 'tariffs_pallet']:
            return self.tariffs(file=file)
        elif name_of_sheet == "statements":
            return self.statements(file=file)
        elif name_of_sheet == "stocks_hard":
            return self.stocks_hard(file=file)
        elif name_of_sheet == NameOfSheet.CardsList:
            return self.cards_list(file=file)
        elif name_of_sheet in [NameOfSheet.SalesFunnel1DayBefore, NameOfSheet.SalesFunnel2DaysBefore]:
            return self.sales_funnel(file=file)
        else:
            print(file)
            sys.exit("I can't convert =(")

    def list_with_dict(self, file: list) -> tuple[list, int, list | None]:
        keys = list()
        for key in file[0].keys():
            keys.append(key)
        ans = numpy.array([keys])
        for i, row in enumerate(file):
            values = list()
            for key, value in row.items():
                values.append(value)
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def list_with_dict_without_numpy(self, file: list) -> tuple[list, int, list | None]:
        keys = list()
        for key in file[0].keys():
            keys.append(key)
        ans = [keys]
        for i, row in enumerate(file):
            values = list(row.values())
            good_values = list()
            for value in values:
                if not (value is list or value is dict):
                    good_values.append(value)
            ans.append(good_values)
        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def products(self, file: dict[str, dict[str, list[int | str | dict[str, str | int | list | dict]]]]):
        if len(file["data"]["items"]) == 0:
            return list(), 0, list()
        keys = list()
        for key in file["data"]["items"][0].keys():
            if key == "metrics":
                continue
            keys.append(key)
        for key in file["data"]["items"][0]["metrics"].keys():
            if key == "avgOrdersByMonth":
                keys.append(key + "Start")
                keys.append(key + "End")
                keys.append(key + "Value")
            elif key in ["saleRate", "avgStockTurnover", "officeMissingTime"]:
                keys.append(key + "InHours")
            elif key == "currentPrice":
                keys.append("currentPrice" + "MinPrice")
                keys.append("currentPrice" + "MaxPrice")
            else:
                keys.append(key)
        ans = [keys]

        for item in file["data"]["items"]:
            row = list()
            for key, value in item.items():
                if key == "metrics":
                    continue
                row.append(value)

            for key, value in item["metrics"].items():
                if key == "avgOrdersByMonth":
                    row.append(value[0]["start"])
                    row.append(value[0]["end"])
                    row.append(value[0]["value"])
                elif key in ["saleRate", "avgStockTurnover", "officeMissingTime"]:
                    row.append(value["days"] * 24 + value["hours"])
                elif key == "currentPrice":
                    row.append(value["minPrice"])
                    row.append(value["maxPrice"])
                else:
                    row.append(value)
            ans.append(row)

        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def orders_not_today(self, file: list) -> tuple[list, int, list | None]:
        keys = list()
        for key in file[0].keys():
            keys.append(key)
        ans = numpy.array([keys])
        for i, row in enumerate(file):
            values = list()
            for key, value in row.items():
                values.append(value)
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        need_to_delete = list()
        for i in range(len(ans)):
            if str(ans[i][1]).startswith(datetime.datetime.now().strftime('%Y-%m-%d')):
                need_to_delete.append(i)
        ans = numpy.delete(ans, need_to_delete, axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def sales_not_today(self, file: dict) -> tuple[list, int, list | None]:
        keys = list()
        for key in file[0].keys():
            keys.append(key)
        ans = numpy.array([keys])
        for i, row in enumerate(file):
            values = list()
            flag = False
            for key, value in row.items():
                if key == "lastChangeDate" and datetime.date(int(value[0:3]), int(value[5:7]),
                                                             int(value[8:10])) == datetime.date.today():
                    flag = True
                values.append(value)
            if flag:
                continue
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def prices(self, file: dict) -> tuple[list, int, list | None]:
        file = file["data"]["listGoods"]
        keys = list()
        for key, value in file[0].items():
            if type(value) is list:
                keys.extend([key for key, value in value[0].items()])
            else:
                keys.append(key)
        ans = list()
        ans.append(keys)
        # print(json.dumps(file, ensure_ascii=False, indent=4))
        for i, row in enumerate(file):
            ans.append([])
            for key, value in row.items():
                if type(value) is list:
                    ans[i + 1].extend([value for key, value in value[0].items()])
                else:
                    ans[i + 1].append(value)
        ans = list(map(lambda x: list(map(lambda y: str(y), x)), ans))
        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def tariffs(self, file: dict) -> tuple[list, int, list | None]:
        with open('plugins/Wildberries/data/date_of_tariffs.txt', 'w') as txt:
            txt.write(file['response']['data']['dtTillMax'])
        keys = list()
        for key in file['response']['data']['warehouseList'][0].keys():
            keys.append(key)
        ans = numpy.array([keys])
        for i, row in enumerate(file['response']['data']['warehouseList']):
            values = list()
            for key, value in row.items():
                values.append(value)
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def statements(self, file: list) -> tuple[list, int, list | None]:
        keys = list()
        for key, value in file[0].items():
            keys.append(key)
        ans = list()
        ans.append(keys)
        # print(json.dumps(file, ensure_ascii=False, indent=4))
        for i, row in enumerate(file):
            ans.append([])
            for key, value in row.items():
                ans[i + 1].append(value)
        ans = list(map(lambda x: list(map(lambda y: str(y), x)), ans))
        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def stocks_hard(self, file):
        keys = ["brand", "subjectName", "vendorCode", "nmId", "barcode", "techSize", "volume", "В пути до получателей",
                "В пути возвраты на склад WB", "Всего находится на складах"]
        keys.extend(file["warehouses"])
        ans = [keys]
        for element in file["json"]:
            ans.append([""] * len(keys))
            for key, value in element.items():
                if key != "warehouses":
                    ans[-1][keys.index(key)] = value
                    continue

                ans[-1].append("0")
                ans[-1].append("0")
                ans[-1].append("0")
                ans[-1].extend([""] * len(file["warehouses"]))
                for warehouse in value:
                    if warehouse["warehouseName"] == "В пути до получателей":
                        ans[-1][7] = warehouse["quantity"]
                        continue
                    elif warehouse["warehouseName"] == "В пути возвраты на склад WB":
                        ans[-1][8] = warehouse["quantity"]
                        continue
                    elif warehouse["warehouseName"] == "Всего находится на складах":
                        ans[-1][9] = warehouse["quantity"]
                        continue

                    try:
                        index = keys.index(warehouse["warehouseName"])
                    except ValueError:
                        for name in keys:
                            if warehouse["warehouseName"] in name:
                                ans[-1][keys.index(name)] = warehouse["quantity"]
                                break
                        else:
                            keys.append(warehouse["warehouseName"])
                            ans[-1].append(warehouse["quantity"])
                    else:
                        try:
                            ans[-1][index] = warehouse["quantity"]
                        except IndexError:
                            ans[-1].append(warehouse["quantity"])

        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def cards_list(self, file):
        ans = list()
        keys = ['nmID', 'imtID', 'nmUUID', 'subjectID', 'subjectName', 'vendorCode', 'brand', 'title', 'description',
                'needKiz', 'photos', 'video', 'length', 'width', 'height', 'weight', 'isValid', 'characteristics',
                'sizes', 'tag_ids', 'tag_names', 'createdAt', 'updatedAt']
        ans.append(keys)

        for row in file:
            ans.append([""] * len(keys))
            for key, value in row.items():
                if key == "photos":
                    photos = ""
                    for photo in value:
                        photos = photos + ";".join(list(photo.values()))
                    ans[-1][keys.index(key)] = photos
                elif key == "dimensions":
                    ans[-1][keys.index("length")] = value["length"]
                    ans[-1][keys.index("width")] = value["width"]
                    ans[-1][keys.index("height")] = value["height"]
                    ans[-1][keys.index("weight")] = value["weightBrutto"]
                    ans[-1][keys.index("isValid")] = value["isValid"]
                elif key == "tags":
                    ans[-1][keys.index("tag_ids")] = ";".join(list(map(lambda x: str(x["id"]), value)))
                    ans[-1][keys.index("tag_names")] = ";".join(list(map(lambda x: x["name"], value)))
                else:
                    ans[-1][keys.index(key)] = value

        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def sales_funnel(self, file):
        keys = ["nmID", "vendorCode", "brandName", "objectId", "objectName", "openCardCount", "addToCartCount",
                "ordersCount", "ordersSumRub", "buyoutsCount", "buyoutsSumRub", "cancelCount", "cancelSumRub",
                "avgPriceRub", "avgOrdersCountPerDay", "addToCartPercent", "cartToOrderPercent", "buyoutsPercent",
                "stocksMp", "stocksWb"]
        ans = [keys]
        for row in file:
            ans.append([
                row["nmID"],
                row["vendorCode"],
                row["brandName"],
                row["object"]["id"],
                row["object"]["name"],
                row["statistics"]["selectedPeriod"]["openCardCount"],
                row["statistics"]["selectedPeriod"]["addToCartCount"],
                row["statistics"]["selectedPeriod"]["ordersCount"],
                row["statistics"]["selectedPeriod"]["ordersSumRub"],
                row["statistics"]["selectedPeriod"]["buyoutsCount"],
                row["statistics"]["selectedPeriod"]["buyoutsSumRub"],
                row["statistics"]["selectedPeriod"]["cancelCount"],
                row["statistics"]["selectedPeriod"]["cancelSumRub"],
                row["statistics"]["selectedPeriod"]["avgPriceRub"],
                row["statistics"]["selectedPeriod"]["avgOrdersCountPerDay"],
                row["statistics"]["selectedPeriod"]["conversions"]["addToCartPercent"],
                row["statistics"]["selectedPeriod"]["conversions"]["cartToOrderPercent"],
                row["statistics"]["selectedPeriod"]["conversions"]["buyoutsPercent"],
                row["stocks"]["stocksMp"],
                row["stocks"]["stocksWb"]
            ])
        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    @staticmethod
    def download(file: dict, name: str) -> str:
        match name:
            case 'statements':
                with open('data/Финансовые отчёты.json', 'w') as d:
                    # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                    json.dump(file, d, ensure_ascii=False, indent=4)
            case 'statements_old':
                with open('data/Финансовые отчёты.json', 'w') as d:
                    # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                    json.dump(file, d, ensure_ascii=False, indent=4)
        return 'download'

    @staticmethod
    def check_keys(keys: list) -> list | None:
        need_to_check = ['nmId', 'nmID', 'nm_id']
        needed_keys = list()
        for i in need_to_check:
            if i in keys:
                n = keys.index(i)
                needed_keys.append(n)
        if needed_keys == []:
            return
        else:
            return needed_keys
        # if 'nmId' in keys:
        #     n = keys.index('nmId')
        #     needed_keys.append(n)
        #     return needed_keys
        # else:
        #     return

    @staticmethod
    def beta_start(file: list) -> tuple[list, int]:
        if type(file) is type(None):
            sys.exit('file = None')
        ans = list()
        ans.append([])
        for key in file[0].keys():
            ans[0].append(key)
        # print(json.dumps(file, ensure_ascii=False, indent=4))
        for i, row in enumerate(file):
            ans.append([])
            for key, value in row.items():
                ans[i + 1].append(value)
        return ans, len(ans)
