import json
import sys
import numpy


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


def convert_to_list(file: list) -> tuple[list, int]:
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
