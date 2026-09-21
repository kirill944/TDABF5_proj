import json


def load_instruments(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        instruments = json.load(file)
    return instruments


def save_instruments(filename, instruments):
    with open(filename, 'r', encoding='UTF-8') as file:
        json.dump(instruments, file, ensure_ascii=False, indent=4)
