import math


instrument_name = "Скрипка"
cost = 15999.99
is_booked = True

def add_instrument(instrument_name, price):
    return f"Инструмент {instrument_name} добавлен по цене {price}"

def change_price(instrument_name, new_price):
    return f"Цена {instrument_name} изменена на {new_price}"

def change_booking_status(instrument_name, is_booked):
    if is_booked:
        is_booked = False
        return f"Инструмент {instrument_name} готов к покупке"
    is_booked = True
    return f"Инструмент {instrument_name} забронирован для покупки"

print(f"Инструмент: {instrument_name}")
print(f"Стоимость: {cost} рублей (Наличными: {math.floor(cost)})")
print(change_booking_status(instrument_name, is_booked))
