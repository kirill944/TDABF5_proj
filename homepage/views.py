from django.shortcuts import render
from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с общим каркасом и Bootstrap 5.3."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
<nav class="nav">
    <a class="nav-link" href="/">Главная</a>
    <a class="nav-link" href="/instruments/">Инструменты</a>
    <a class="nav-link" href="/bookings/">Бронирования</a>
</nav>
<main class="container mt-4">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Instrument Booking</h1>
    <p class="lead">Система бронирования музыкальных инструментов.</p>
    <p>Основные разделы:</p>
    <a href="/instruments/" class="btn btn-primary me-2">Инструменты</a>
    <a href="/bookings/" class="btn btn-secondary">Бронирования</a>
    """
    return HttpResponse(page("Instrument Booking", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )