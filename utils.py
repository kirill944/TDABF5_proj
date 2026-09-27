"""Вспомогательные функции ввода."""
from datetime import datetime


def input_int(prompt: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Введены неверные данные, попробуйте снова')


def input_date(prompt: str) -> str:
    """Безопасный ввод даты в формате YYYY-MM-DD."""
    while True:
        value = input(prompt)
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            print('Неверный формат даты, используйте YYYY-MM-DD')
