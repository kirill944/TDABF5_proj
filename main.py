from instruments import *


def show_instruments(instruments):
    """Вывести список помещений.
    TODO: перебрать список instruments и вывести помещения
    в виде таблицы.
    """
    pass


def show_bookings(bookings):
    """Вывести список бронирований.
    TODO: перебрать словарь bookings и вывести бронирования
    с указанием инструментов.
    """
    pass


def main():
    instruments = []
    while True:
        print('1. Добавить инструмент')
        print('2. Найти инструмент')
        print('0. Выход')
        case = input()
        if case == '0':
            break
        if case == '1':
            instrument_name = input('Введите название инструмента: ')
            price = int(input('Введите цену инструмента: '))
            instruments = add_instrument(instruments, instrument_name, price)
        if case == '2':
            instrument_name = input('Введите название инструмента: ')
            print(find_instrument(instruments, instrument_name))




if __name__ == "__main__":
    main()
