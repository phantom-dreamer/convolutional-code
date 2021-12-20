import random

from file_handling import read_file, write_to_file
from config_parser import json_parser
from binary_math import xor


def xor_with_memory(text, g_indexes_list, memory_register_length, with_symbol=False):
    result = ''
    memory_register = ['0'] * memory_register_length
    for symbol in text:
        memory_register.insert(0, symbol)
        memory_register.pop(-1)
        if with_symbol:
            result += symbol
        for polynomial_index in g_indexes_list:
            result += xor([memory_register[i] for i in polynomial_index])
    return result, memory_register


def coder(text, g_indexes_list, memory_register_length):
    result, memory_register = xor_with_memory(text, g_indexes_list, memory_register_length, with_symbol=True)
    memory_register.insert(0, '0')
    memory_register.pop(-1)
    result += '0'
    for polynomial_index in g_indexes_list:
        result += xor([memory_register[i] for i in polynomial_index])
    return result


def decoder(encoded, g_indexes_list, memory_register_length, n):
    q = 0
    information_bits = encoded[::n]
    check_bits = ''
    for i in range(1, len(encoded), n):
        check_bits += encoded[i:i+n-1]
    result = ''
    check_decoder_bits, memory_register = xor_with_memory(information_bits, g_indexes_list, memory_register_length)
    check_decoder_bits = list(check_decoder_bits)

    for i in range(len(information_bits) - 1):
        m = n-1
        if check_bits[i*m:i*m + m] != ''.join(check_decoder_bits[i*m:i*m + m]):
            q += 1
        if check_bits[(i+1)*m:(i+1)*m + m] != ''.join(check_decoder_bits[(i+1)*m:(i+1)*m + m]):
            q += 1
        if q == 2:
            new_el = '1' if information_bits[i] == '0' else '0'
            result += new_el
            information_bits = information_bits[:i] + new_el + information_bits[i+1:]
            check_decoder_bits, memory_register = xor_with_memory(
                information_bits,
                g_indexes_list,
                memory_register_length
            )
            check_decoder_bits = list(check_decoder_bits)
        else:
            result += information_bits[i]
        q = 0
    return result


def make_error(encoded):
    random_index = random.randint(0, len(encoded) - 1)
    result = encoded[:random_index]
    result += '1' if encoded[random_index] == '0' else '0'
    result += encoded[random_index+1:]
    return result


def convolutional_communication_channel(file, config_name=r'config.json', dir_to_write='decode'):
    n, k,  g_indexes_list = json_parser(config_name)
    memory_register_length = max(g_indexes_list, key=lambda x: max(x))[-1] + 1
    write_to_file(file=file, text='', mode='wb', dir_to_write=dir_to_write)
    step = n
    for text in read_file(file):
        decoded = ''
        for i in range(0, len(text), step):
            s = coder(text[i:i + step], g_indexes_list, memory_register_length)
            v = make_error(s)
            decoded += ''.join(str(s) for s in decoder(v, g_indexes_list, memory_register_length, n)[:len(text[i:i + step])])
        write_to_file(file=file, text=decoded, mode='ab', dir_to_write=dir_to_write)
