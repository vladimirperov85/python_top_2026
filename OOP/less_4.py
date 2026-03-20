
class Account:
    def __init__(self):
        self.__name = ''
        self.__password = ''

    def set_name(self, new_name):
        self.__name = new_name

    def set_password(self, new_password):
        if len(new_password) > 5:
            self.__password = new_password
            print('пароль установлен')
        else:
            print('Ошибка при установке пароля')
            
    def get_name(self):
        return self.__name
    
    def get_password(self):
        return self.__password
    
    def cheek_password(self, password):
        if password == self.__password:
            return True
        else:
            return False
        
    def cheeek_name(self, name):
        if name == self.__name:
            return True
        else:
            return False
    

    

account = Account()
account.set_name('Иван')
account.set_password('1234567')
account.get_password()
print(account.cheeek_name('Иван'))


class Person:
    def __init__(self, age):
        self.__age = age
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self,new_age):
        if 0 < new_age <= 100:
            self.__age = new_age
        else:
            print('Ошибка!')
    
p = Person(29)
print(p.age)
p.age = 39
print(p.age)

class Water:
    def __init__(self,temp):
        self.__temp = temp

    def get_temp(self):
        return self.__temp
    
    def set_temp(self, new_temp):
        if 0 <= new_temp <= 100:
            self.__temp = new_temp
            print('ok')
        else:
            print("Invalid temperature")
    
    def get_state(self):
        if self.__temp <= 0:
            return "ice"
        elif self.__temp >= 100:
            return "steam"
        else:
            return "water"


w = Water(25)
print(w.get_temp())
print(w.get_state())
w.set_temp(101)


class Animal:
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def speak(self):
        print('Жиотное издало звук')

    def get_info(self):
        print(f'Имя: {self.name}\nВозраст: {self.age}')
        

class Dog(Animal):
    def __init__(self,name,age,bread):
        super().__init__(name,age)

    def speak(self):
        print('Гав')

    def fetch(self):
        print('Поймал')


animal = Animal('Васька', 5)
animal.speak()
animal.get_info()
dog = Dog('Шарик', 5,'Корги')
dog.speak()
dog.fetch()
dog.get_info()


class Parent:
    def __init__(self,name):
        self.name = name
        print('parent create')

    def greet(self):
        print(f'hello I am {self.name}')

class Child(Parent):
    def __init__(self,name,age):
        super().__init__(name)
        self.age = age
        print('chald criated')

    def greet(self):
        super().greet()
        print(f'Мне {self.age} лет')

c = Child('Vasya',12)
c.greet()


class Transport:
    def __init__(self,brend,model,year):
        self.brend=brend
        self.model=model
        self.year=year
    
    def get_info(self):
        print(f"Марка: {self.brend}\nМодель: {self.model}\nГод выпуска: {self.year}")


class Car(Transport):
    def __init__(self,brend,model,year,number_of_doors):
        super().__init__(brend,model,year)
        self.number_of_doors=number_of_doors

    def get_info(self):
        print(f"Марка: {self.brend}\nМодель: {self.model}\nГод выпуска: {self.year}\nКоличество дверей: {self.number_of_doors}")

t = Transport("Audi","A6",2015)
car = Car("Audi","A6",2015,4)
car.get_info()
t.get_info()


