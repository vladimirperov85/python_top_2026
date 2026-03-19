class Dog:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.is_hungry = True

    def bark(self):
        print(f'{self.name} сказала ГАВ-ГАВ')

    def eat(self):
        if self.is_hungry:
            print(f'{self.name} собака поела')
            self.is_hungry = False
        else:
            print(f'{self.name} Не голодна')

    def get_info(self):
        print(f'Собака {self.name} Возраст {self.age} Голодна {self.is_hungry}')


dog1 = Dog('Бобик','3')
dog1.get_info()
dog1.eat()
dog1.bark()
print(dog1)

class User:
    def __init__(self,name,password):
        self.name = name # public
        self._login = 'Login'
        self.__password = password #prived
    def get_password(self):
        return self.__password

    def set_password(self,new_password):
        self.__password = new_password

    def show_info(self):
        print(f'name: {self.name}, password: {self.__password}')


user = User('vladimir','12345')
# print(user.name)
# print(user._login)
# print(user.__password)
print(user.get_password)
user.set_password('6575895')
print(user.get_password())

class Safe:
    def __init__(self,name,money):
        self.__name = name
        self.__money = money

    def get_money(self):
        return self.__money

    def set_money(self,money):
        self.__money = money

    def get_name(self):
        return self.__name

    def pick_up(self,money):
        self.__money -= money


    def add_money(self,money):
        self.__money += money


safe = Safe('Vladimir',100)
print(safe.get_money())
print(safe.get_name())
safe.pick_up(50)
print(safe.get_money())
safe.add_money(100)
print(safe.get_money())


