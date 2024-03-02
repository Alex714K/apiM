import json


def start(file: list):
    ans = list()
    # print(json.dumps(file, ensure_ascii=False, indent=4))
    for i, row in enumerate(file):
        ans.append([])
        for key, value in row.items():
            ans[i].append(value)
    return ans, len(ans)


def beta_start(file: list):
    ans = list()
    dist = len(file)
    # print(json.dumps(file, ensure_ascii=False, indent=4))
    for i, row in enumerate(file):
        if i % 1000 == 0:
            ans.append([])
            print(len(ans[0]))
        ans[0].append([])
        for key, value in row.items():
            ans[0][i].append(value)
    return ans, len(ans)
