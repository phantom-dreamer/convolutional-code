import json


def get_parser_values(data):
    n = data.get('n', None)
    k = data.get('k', None)
    if not n or not k or n < 1 or k !=1:
        raise ValueError(f'Неправильные параметры')
    g_str = 'g'
    g_indexes = []
    for i in range(2, n+1):
        g = data.get(f'{g_str}{str(i)}', None)
        if g:
            if not all(elem == 1 for elem in g):
                raise ValueError(
                    f'Ошибка в полиноме {g_str}{str(i)}, не корректный полином, введите ортогональный полином'
                )
            g_indexes.append([i for i, v in enumerate(g) if v == 1])
        else:
            raise ValueError(f'Полином {g_str}{str(i)} отсутсвует')

    return n, k, g_indexes


def json_parser(name):
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return get_parser_values(data)
