def get_parameters() -> dict:
    """Достаёт словарь параметров в parameters.txt и возвращает его"""
    with open('parameters.txt', 'r') as txt:
        param = txt.read().split('\n')
    param = dict(map(lambda x: x.split('='), param))
    return param
