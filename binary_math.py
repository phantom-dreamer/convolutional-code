def xor(text):
    """ операция сложения по мод 2 """
    if text.count('1') % 2 == 0:
        return '0'
    else:
        return '1'
