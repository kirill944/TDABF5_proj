"""Тесты для класса User и функций работы с пользователями."""
from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, 'Иван Петров', 'ivan@example.com')
    assert user.id == 1
    assert user.name == 'Иван Петров'
    assert user.email == 'ivan@example.com'


def test_user_str():
    user = User(1, 'Иван Петров', 'ivan@example.com')
    assert str(user) == 'Иван Петров <ivan@example.com>'


def test_user_from_data():
    data = {'id': 1, 'name': 'Иван Петров', 'email': 'ivan@example.com'}
    user = User.from_data(data)
    assert user.id == 1
    assert user.name == 'Иван Петров'
    assert user.email == 'ivan@example.com'


def test_user_to_dict():
    user = User(1, 'Иван Петров', 'ivan@example.com')
    assert user.to_dict() == {
        'id': 1,
        'name': 'Иван Петров',
        'email': 'ivan@example.com',
    }


def test_add_user():
    users = []
    add_user(users, 1, 'Иван Петров', 'ivan@example.com')
    assert len(users) == 1
    assert users[0].name == 'Иван Петров'


def test_find_user_by_name():
    users = [User(1, 'Иван Петров', 'ivan@example.com')]
    assert len(find_user(users, 'Иван')) == 1


def test_find_user_by_email():
    users = [User(1, 'Иван Петров', 'ivan@example.com')]
    assert len(find_user(users, 'ivan@')) == 1


def test_find_user_no_match():
    users = [User(1, 'Иван Петров', 'ivan@example.com')]
    assert find_user(users, 'Пётр') == []


def test_find_user_by_id():
    users = [User(1, 'Иван Петров', 'ivan@example.com')]
    assert find_user_by_id(users, 1).name == 'Иван Петров'
    assert find_user_by_id(users, 99) is None
