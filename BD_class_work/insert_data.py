import sqlite3

# Подключаемся к БД
conn = sqlite3.connect('school.db')

# cursor - это специальный объект который позволяет работать с БД
cursor = conn.cursor()


student = [
    (1, 'Ivan', 'Ivanov', '2000-01-01', 'M', '1111111111'),
    (1, 'Ivan', 'Ivanov', '2000-01-01', 'M', '1111111111'),
    (1, 'Ivan', 'Ivanov', '2000-01-01', 'M', '1111111111'),
    (1, 'Ivan', 'Ivanov', '2000-01-01', 'M', '1111111111'),
    (1, 'Ivan', 'Ivanov', '2000-01-01', 'M', '1111111111'),
]