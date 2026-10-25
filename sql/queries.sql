-- 1. Выборка списка (SELECT)
-- Список всех инструментов с сортировкой по цене
SELECT id, name, price FROM instruments ORDER BY price DESC;

-- Список всех пользователей
SELECT id, name, email FROM users ORDER BY name;

-- 2. Фильтрация (WHERE)
-- Поиск инструментов дешевле 15000
SELECT id, name, price FROM instruments WHERE price < 15000;

-- Поиск активных бронирований
SELECT id, instrument_id, booking_date FROM bookings WHERE is_cancelled = 0;

-- 3. Соединение таблиц (JOIN)
-- Полная информация о бронированиях (инструмент + пользователь)
SELECT b.id, b.booking_date, i.name AS instrument_name, u.name AS user_name
FROM bookings b
JOIN instruments i ON b.instrument_id = i.id
JOIN users u ON b.user_id = u.id
WHERE b.is_cancelled = 0;

-- Поиск пользователей, которые бронировали скрипку (через JOIN и WHERE)
SELECT DISTINCT u.name, u.email
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN instruments i ON b.instrument_id = i.id
WHERE i.name = 'Скрипка';

-- 4. Агрегатные функции (COUNT, SUM, AVG, MIN, MAX)
-- Общее количество инструментов
SELECT COUNT(*) AS total_instruments FROM instruments;

-- Общая стоимость всех инструментов в каталоге
SELECT SUM(price) AS total_value FROM instruments;

-- Средняя цена инструмента
SELECT AVG(price) AS average_price FROM instruments;

-- 5. Группировка (GROUP BY)
-- Количество бронирований для каждого инструмента
SELECT i.name AS instrument_name, COUNT(b.id) AS bookings_count
FROM instruments i
LEFT JOIN bookings b ON i.id = b.instrument_id AND b.is_cancelled = 0
GROUP BY i.id, i.name
ORDER BY bookings_count DESC;

-- Количество бронирований, сделанных каждым пользователем
SELECT u.name AS user_name, COUNT(b.id) AS bookings_count
FROM users u
LEFT JOIN bookings b ON u.id = b.user_id
GROUP BY u.id, u.name;

-- 6. Фильтрация групп (HAVING)
-- Инструменты, которые бронировали более 1 раза
SELECT i.name, COUNT(b.id) AS bookings_count
FROM instruments i
JOIN bookings b ON i.id = b.instrument_id
WHERE b.is_cancelled = 0
GROUP BY i.id, i.name
HAVING COUNT(b.id) > 1;

-- 7. Поиск свободных инструментов на выбранную дату (NOT IN)
SELECT id, name, price
FROM instruments
WHERE id NOT IN (
    SELECT instrument_id
    FROM bookings
    WHERE booking_date = ? AND is_cancelled = 0
)
ORDER BY name;