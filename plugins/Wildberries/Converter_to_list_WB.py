import json
import sys
import numpy
import datetime


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
            sys.exit(file)
        if name_of_sheet in ['orders_today', 'sales_today', 'stocks', 'rk']:
            return self.list_with_dict(file=file)
        elif name_of_sheet in "coefficients":
            return self.list_with_dict_without_numpy(file=file)
        elif name_of_sheet in ['orders_1mnth', 'orders_1week', 'orders_2days']:
            return self.orders_not_today(file=file)
        elif name_of_sheet in ['prices', 'fixed_prices']:
            return self.prices(file=file)
        elif name_of_sheet in ['tariffs_boxes', 'tariffs_pallet']:
            return self.tariffs(file=file)
        elif name_of_sheet == 'statements':
            return self.statements(file=file)
        elif name_of_sheet == 'storage_paid':
            return self.list_with_dict(file=file)
        elif name_of_sheet == 'stocks_hard':
            return self.stocks_hard(file=file)
        else:
            print(file)
            return sys.exit("I can't convert =(")

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
            ans.append(list(row.values()))
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
            if datetime.datetime.now().strftime('%Y-%m-%d') == str(ans[i][1])[:10]:
                need_to_delete.append(i)
        ans = numpy.delete(ans, need_to_delete, axis=0)
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
                    ans[i+1].extend([value for key, value in value[0].items()])
                else:
                    ans[i+1].append(value)
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
                ans[i+1].append(value)
        ans = list(map(lambda x: list(map(lambda y: str(y), x)), ans))
        needed_keys = self.check_keys(keys)
        return ans, len(ans), needed_keys

    def stocks_hard(self, file):
        keys = ["brand", "subjectName", "vendorCode", "nmId", "barcode", "techSize", "volume", "inWayToClient",
                         "inWayFromClient", "quantityWarehousesFull"]
        keys.extend(file["warehouses"])
        ans = [keys]
        for element in file["json"]:
            ans.append(list(element.values())[:-1])
            ans[-1].extend([""] * len(file["warehouses"]))
            for warehouse in element["warehouses"]:
                try:
                    ans[-1][keys.index(warehouse["warehouseName"])] = warehouse["quantity"]
                except ValueError:
                    for key in keys:
                        if warehouse["warehouseName"] in key:
                            ans[-1][keys.index(key)] = warehouse["quantity"]

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
                ans[i+1].append(value)
        return ans, len(ans)
