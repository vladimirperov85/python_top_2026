import sqlite3

# Подключаемся к БД
conn = sqlite3.connect('school.db')

# cursor - это специальный объект который позволяет работать с БД
cursor = conn.cursor()

# создание таблицы учеников
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    grade INTEGER CHECK(grade BETWEEN 1 AND 11)
)
""")

# создание таблицы предметов
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

# создание таблицы оценок
cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES students(id),
    subject_id INTEGER REFERENCES subjects(id),
    score INTEGER CHECK(score BETWEEN 1 AND 5)
)
""")

# сохраняем изменения
conn.commit()
print('Таблицы созданы')

# Проверяем, что таблицы действительно создались
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Список таблиц в БД:")
for table in tables:
    print(f"  - {table[0]}")

# закрываем соединение
conn.close()

