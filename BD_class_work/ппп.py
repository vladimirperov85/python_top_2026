import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Добавляем учеников
cursor.execute("INSERT INTO students (name, email, grade) VALUES (?, ?, ?)", 
               ('Иван Петров', 'ivan@school.ru', 10))
cursor.execute("INSERT INTO students (name, email, grade) VALUES (?, ?, ?)", 
               ('Мария Сидорова', 'maria@school.ru', 11))

# Добавляем предметы
cursor.execute("INSERT INTO subjects (name) VALUES (?)", ('Математика',))
cursor.execute("INSERT INTO subjects (name) VALUES (?)", ('Физика',))

# Добавляем оценки
cursor.execute("INSERT INTO grades (student_id, subject_id, score) VALUES (?, ?, ?)", 
               (1, 1, 5))  # Иван - Математика - 5
cursor.execute("INSERT INTO grades (student_id, subject_id, score) VALUES (?, ?, ?)", 
               (1, 2, 4))  # Иван - Физика - 4
cursor.execute("INSERT INTO grades (student_id, subject_id, score) VALUES (?, ?, ?)", 
               (2, 1, 3))  # Мария - Математика - 3

conn.commit()
conn.close()
print('Данные добавлены!')