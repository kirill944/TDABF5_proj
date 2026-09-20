def add_instrument(instruments: list[dict],
                   instrument_name: str, price: int) -> list[dict]:
    instruments.append({'name': instrument_name, 'price': price})
    print(f"Инструмент {instrument_name} добавлен по цене {price}")
    return instruments


def find_instrument(instruments: list[dict[str, int]],
                    instrument_name: str) -> bool:
    for instrument in instruments:
        if instrument['name'] == instrument_name:
            return True
    return False


def delete_instrument(instruments: list[dict],
                      instrument_name: str) -> list[dict]:
    for instrument in instruments:
        if instrument['name'] == instrument_name:
            instruments.remove(instrument)
    print(f"Инструмент {instrument_name} удален")
    return instruments


def change_price(instrument_name: str, new_price: int) -> None:
    print(f"Цена {instrument_name} изменена на {new_price}")
