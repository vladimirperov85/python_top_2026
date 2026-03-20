
# Задание 1:
# 1. Создайте класс Wolf (Волк).
# o Метод howl() — выводит "Уууу!".
# 2. Создайте класс Dog (Собака).
# o Метод bark() — выводит "Гав!".
# 3. Создайте класс Werewolf (Оборотень), который наследуется от Wolf и Dog.
# 4. Добавьте свой метод transform() — выводит "Превращение!"


# class Wolf:

#     def howl(self):
#         print(f"УУУ!")

# class Dog:

#     def bark(self):
#         print(f"Гав!")

# class Werewolf(Wolf, Dog):

#     def transform(self):
#             print(f'Превращение')

# #проверки
# werewolf = Werewolf()
# werewolf.howl()
# werewolf.bark()
# werewolf.transform()
# Werewolf.__mro__


# Задание 2:
# 1. Создайте миксин EatMixin с методом eat() — выводит "Сотрудник ест".
# 2. Создайте миксин SleepMixin с методом sleep() — выводит "Сотрудник спит".
# 3. Создайте класс Worker, который наследуется от EatMixin и SleepMixin.
# o Атрибут: name (имя).
# o Метод work() — выводит "[Имя] работает".


# class EatMixin:
#     def eat(self):
#         print("Сотрудник ест")

# class SleepMixin:
#     def sleep(self):
#         print("Сотрудник спит")

# class Worker(EatMixin, SleepMixin):
#     def __init__(self, name):
#         self.name = name

#     def work(self):
#         print(f"{self.name} работает")

# #проверки
# worker = Worker("Иван")
# worker.eat()
# worker.sleep()
# worker.work()


# Задание 3:
# 1. Создайте класс A с методом show() — выводит "Класс A".
# 2. Создайте класс B с методом show() — выводит "Класс B".
# 3. Создайте класс C, который наследуется от A и B в таком порядке: class C(A, B):.
# 4. В классе C создайте метод test(), который вызывает self.show().

# class A:
#     def show(self):
#         print("Класс A")

# class B:
#     def show(self):
#         print("Класс B")

# # class C(A, B):
# #     def test(self):
# #         self.show()

# class C(B, A):
#     def test(self):
#         self.show()

#проверки
# с = C()
# с.test()
# C.mro() # метод mro() выводит порядок наследования классов - и если вызвать этот метод станет очеревидно
# что класс С наследуется от класса А и только затем от класса В - поэтому будет вызван метод show() класса A,
# если мы меняем порядок наследования на B, A - то будет вызван метод show() класса B


# Задание 4:
# 1. Создайте миксин PrintMixin с методом print_document(text) — выводит текст в
# консоль.
# 2. Создайте миксин SaveMixin с методом save_document(text) — выводит "Сохранено:
# [text]".
# 3. Создайте класс Document, который наследуется от обоих миксинов.
# 4. Добавьте метод create(content) — создаёт документ и использует оба миксина.

# class PrintMixin:
#     def print_document(self, text):
#         print(text)

# class SaveMixin:
#     def save_document(self, text):
#         print(f"Сохранено: {text}")

# class Document(PrintMixin, SaveMixin):
#     def create(self, content):
#         self.print_document(content)

# проверки
# document = Document()
# document.create('Важный документ')
# document.save_document('Важный документ')
