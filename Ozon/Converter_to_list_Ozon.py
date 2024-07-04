import json
import sys
import numpy
import datetime
import logging


class Converter:
    def convert_to_list(self,
                        file: list | dict, name_of_sheet: str) -> (tuple[list, int, list | None] | str):
        """Конвертирует json-объект в список, который подходит для добавления данных из файла в Google Excel"""
        match file:
            case None:
                return 'is None'
            case []:
                return 'is empty'
        if name_of_sheet == 'analytics':
            return self.analytics(file=file)
        elif name_of_sheet == 'stock_on_warehouses':
            return self.stock_on_warehouses(file=file)
        elif name_of_sheet == 'products':
            return self.products(file=file)

    def products(self, file):
        keys = ["code", "status", "error", "file", "report_type", "params", "created_at"]
        ans = [keys, list(file["result"].values())]
        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def stock_on_warehouses(self, file):
        keys = ["sku", "warehouse_name", "item_code", "item_name", "promised_amount", "free_to_sell_amount",
                "reserved_amount"]
        ans = numpy.array([keys])
        for row in file:
            values = list()
            values.extend(row.values())
            # используем numpy для быстроты программы
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def analytics(self, file: list) -> tuple[list, int, list | None]:
        keys = ["sku_id", "sku_name", "day", "revenue", "ordered_units", "hits_view_search", "hits_view_pdp",
                "hits_view", "hits_tocart_search", "hits_tocart_pdp", "hits_tocart", "session_view_search",
                "session_view_pdp", "session_view", "conv_tocart_search", "conv_tocart_pdp", "conv_tocart", "returns",
                "cancellations", "delivered_units", "position_category"]
        ans = numpy.array([keys])
        for row in file:
            values = list()
            dimensions = row["dimensions"]
            # добавляем dimensions
            values.append(dimensions[0]["id"])
            values.append(dimensions[0]["name"])
            values.append(dimensions[1]["id"])
            # добавляем metrics
            values.extend(row["metrics"])
            # используем numpy для быстроты программы
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    @staticmethod
    def check_keys(keys: list) -> list | None:
        need_to_check = []
        needed_keys = list()
        for i in need_to_check:
            if i in keys:
                n = keys.index(i)
                needed_keys.append(n)
        return needed_keys
        # if 'nmId' in keys:
        #     n = keys.index('nmId')
        #     needed_keys.append(n)
        #     return needed_keys
        # else:
        #     return

    @staticmethod
    def download(file: dict, name: str) -> str:
        match name:
            case 'statements':
                with open('../Финансовые отчёты.json', 'w') as d:
                    # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                    json.dump(file, d, ensure_ascii=False, indent=4)
            case 'statements_old':
                with open('../Финансовые отчёты.json', 'w') as d:
                    # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                    json.dump(file, d, ensure_ascii=False, indent=4)
        return 'download'

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
