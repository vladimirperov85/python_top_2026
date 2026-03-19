# Задание 1:
# 1. Создайте родительский класс Shape (Фигура).
# 2. Атрибуты: color (цвет), filled (заполненная или нет).
# 3. Метод get_info() — выводит цвет и заполненность.
# 4. Создайте дочерний класс Rectangle (Прямоугольник).
# 5. Добавьте атрибуты: width, height.
# 6. Переопределите get_info() — добавьте размеры.
# 7. Добавьте метод get_area() — возвращает площадь.

class Share:
    def __init__(self,color,filed):
        self.color = color
        self.filed = filed

    def get_info(self):
        print(f'Цвет: {self.color},Заполненность {self.filed}')


class Rectangle(Share):
    def __init__(self,color,filed,width,height):
        super().__init__(color,filed)
        self.width = width
        self.height = height

    def get_info(self):
        print(f'Цвет: {self.color},Заполненность {self.filed},Ширина {self.width},Высота {self.height}')

    def get_area(self):
        return f'Плошадь прямоугольника: {self.width * self.height}'


# проверки
share = Share('Красный','100%')
rectangle = Rectangle('Синий','100%',10,20)
share.get_info()
rectangle.get_info()
print(rectangle.get_area())



# Задание 2:
# 1. Создайте родительский класс User.
# 2. Атрибуты: username, email.
# 3. Метод login() — выводит "Пользователь [username] вошёл".
# 4. Метод get_permissions() — возвращает список ["read"].
# 5. Создайте дочерний класс Admin.
# 6. Переопределите get_permissions() — возвращает ["read", "write", "delete"].
# 7. Добавьте метод ban_user(user) — выводит "Админ забанил [username]".


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def Login(self):
        print(f'Пользователь {self.username} вошёл')

    def get_permissions(self):
        return ['read']

class Admin(User):

    def get_permissions(self):
        return ['read', 'write', 'delete']

    def ban_user(self, user):
        print(f'Админ забанил пользователя -  {user}')


# проверки
user = User('Алексей', 'alex@mail.ru')
admin = Admin('Админ', 'admin@mail.ru')
user.Login()
admin.Login()
print(*user.get_permissions())
print(*admin.get_permissions())
admin.ban_user('Алексей')


# Задание 3:
# 1. Создайте класс Device (Устройство).
# o Атрибуты: brand, model, price.
# o Метод get_info() — основная информация.
# o Метод turn_on() — "Устройство включено".
# 2. Создайте класс Phone (наследуется от Device).
# o Добавьте атрибут: phone_number.
# o Переопределите turn_on() — "Телефон включён".
# o Добавьте метод call(number) — "Звонок на [number]".
# 3. Создайте класс Smartphone (наследуется от Phone).
# o Добавьте атрибут: os (операционная система).
# o Переопределите turn_on() — "Смартфон включён с [os]".
# o Добавьте метод install_app(app_name) — "Установлено приложение
# [app_name]".


class Device:
    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price

    def get_info(self):
        print(f'Бренд: {self.brand}, Модель: {self.model}, Цена: {self.price}')

    def turn_on(self):
        print('Устройство включено')

class Phone(Device):
    def __init__(self, brand, model, price, phone_number):
        super().__init__(brand, model, price)
        self.phone_number = phone_number

    def turn_on(self):
        print('Телефон включён')

    def call(self, number):
        print(f'Звонок на {number}')

class Smartphone(Phone):
    def __init__(self, brand, model, price, phone_number, os):
        super().__init__(brand, model, price, phone_number)
        self.os = os

    def turn_on(self):
        print(f'Смартфон включён с {self.os}')

    def install_app(self, app_name):
            print(f"Установлено приложение '{app_name}' ")


# проверки
device = Device('Notebook', 'i5', 13500)
phone = Phone('Samsung', 'A51', 10000, '+79111111111')
smartphone = Smartphone('Apple', 'iPhone 13', 900000, '+7922222222', 'IOS')
device.turn_on()
smartphone.turn_on()
phone.turn_on()
phone.call('+79111111111')
smartphone.install_app('WhatsApp')
device.get_info()
phone.get_info()
smartphone.get_info()
