import os
import bitstring



def read_file(file):
    binary_file = bitstring.ConstBitStream(filename=file)
    bit_array_length = 512
    iter_count = len(binary_file) // bit_array_length if not len(binary_file) % bit_array_length else len(binary_file) // bit_array_length + 1
    for i in range(iter_count):
        if binary_file.pos + bit_array_length > len(binary_file):
            data = binary_file.read(len(binary_file) - binary_file.pos)
        else:
            data = binary_file.read(bit_array_length)
        yield data.bin


def write_to_file(file, text, mode='ab', dir_to_write='decode'):
    file_name = os.path.abspath(os.path.join(dir_to_write, os.path.basename(file)))
    try:
        with open(file_name, mode) as f:
            bitstring.Bits(bin=text).tofile(f)
    except PermissionError:
        write_to_file(file, text, mode, dir_to_write)
