import time
from convolutional_code import convolutional_communication_channel


def main():
    time_to_start = time.time()
    convolutional_communication_channel(file='t3.txt', config_name='config.json')
    time_to_end = time.time()
    print(f'Функция работала {time_to_end - time_to_start} секунд')


if __name__ == '__main__':
    main()
