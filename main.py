import math


instrument_name = "Скрипка"
cost = 15999.99
is_booked = True

def get_booking_status(is_booked):
    if is_booked:
        return "Инструмент забронирован для покупки"
    return "Инструмент готов к покупке"

print(f"Инструмент: {instrument_name}")
print(f"Стоимость: {cost} рублей (Наличными: {math.floor(cost)})")
print(get_booking_status(is_booked))
