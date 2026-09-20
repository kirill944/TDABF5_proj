from instruments import add_instrument, delete_instrument, find_instrument


def test_add_instrument():
    instruments = [{'name': 'Виолончель', 'price': 70000}]
    instruments = add_instrument(instruments, 'Скрипка', 10000)
    assert len(instruments) == 2


def test_delete_instrument():
    instruments = [{'name': 'Виолончель', 'price': 70000}]
    instruments = delete_instrument(instruments, 'Виолончель')
    assert len(instruments) == 0


def test_find_instrument():
    instruments = [{'name': 'Виолончель', 'price': 70000}]
    is_ins = find_instrument(instruments, 'Виолончель')
    assert is_ins is True
