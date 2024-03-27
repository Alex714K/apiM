import json
import sys
import numpy


def beta_start(file: list) -> tuple[list, int]:
    """Конвертирует json-объект в список, который подходит для добавления данных из файла в Google Excel"""
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


def convert_to_list(file: (list, dict), name_of_sheet: str) -> tuple[list, int]:
    if name_of_sheet in ['orders_1mnth', 'orders_1week', 'orders_2days', 'orders_today', 'stocks', 'rk']:
        return orders(file=file)
    elif name_of_sheet == 'prices':
        return goods(file=file)
    elif name_of_sheet in ['tariffs_boxes', 'tariffs_pallet']:
        return tariffs(file)
    elif name_of_sheet == 'rk':
        return rk(file)


def orders(file: list) -> tuple[list, int]:
    """Конвертирует json-объект в список, который подходит для добавления данных из файла в Google Excel"""
    if type(file) is type(None):
        sys.exit('file = None')
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
    return ans.tolist(), ans.shape[0]


def goods(file: dict) -> tuple[list, int]:
    if type(file) is type(None):
        sys.exit('file = None')
    file = file["data"]["listGoods"]
    ans = list()
    ans.append([])
    for key, value in file[0].items():
        if type(value) is list:
            ans[0].extend([key for key, value in value[0].items()])
        else:
            ans[0].append(key)
    # print(json.dumps(file, ensure_ascii=False, indent=4))
    for i, row in enumerate(file):
        ans.append([])
        for key, value in row.items():
            if type(value) is list:
                ans[i+1].extend([value for key, value in value[0].items()])
                # ans[i+1].append()
            else:
                ans[i+1].append(value)
    for i in range(len(ans)):
        ans[i] = list(map(lambda x: str(x), ans[int(i)]))
    return ans, len(ans)


def tariffs(file: dict) -> tuple[list, int]:
    if type(file) is type(None):
        sys.exit('file = None')
    with open('date_of_tariffs.txt', 'w') as txt:
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
    return ans.tolist(), ans.shape[0]


def rk(file: dict) -> tuple[list, int]:
    pass
