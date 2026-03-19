import time
class Employee:
    def __init__(self, name,salary):
        self.name = name
        self.salary = salary

    def bunus(self):
        return 0
    
class Manager (Employee):
    def __init__(self, name,salary,team_size):
        super().__init__(name,salary)
        self.team_size = team_size 
    
    
    def bunus(self):
        return self.salary * 0.1
    



emp = Employee('Petr',50000)
print(emp.bunus())
print(f'{emp.name} {emp.salary}')

mgr = Manager('IVAN',1000000,10)
print(mgr.bunus())




class LogMixin:
    def log(self,message):
        print(f'[log] {message}')

class SaveMixin:
    def save(self):
        print('Сохранено в базу данных')

class User(LogMixin,SaveMixin):
    def __init__(self,name):
        self.name = name

    def register(self):
        self.log(f'{self.name} registered')
        self.save()



u = User('Petr')
u.register()




class Car:
    def drive(self):
        print("Машина едит")

class Plane:
    def fly(self):
        print('Самолет летит')

class FlyingCar(Car, Plane):
    pass




f = FlyingCar()
f.fly()
f.drive()



class TimeMicin:
    def get_time(self):
        return time.time()

class Tasks(TimeMicin):
    def __init__(self,name):
        self.name = name

    def time_input(self):
        return self.get_time()
    


task = Tasks("task1")
task.time_input()

class A:
    def __init__(self):
        print('A init')


class B(A):
    def __init__(self):
        print('B init')
        super().__init__()

class C(A):
    def __init__(self):
        print('C init')
        super().__init__()    

class D(B,C):
    def __init__(self):
        print('D init')
        super().__init__()


d = D()
print(D.mro())




class LogMixin:
    def log(self, message, level='INFO'):  # Исправлено: IFO → INFO
        print(f'{level} {self.__class__.__name__} {message}')  # Исправлено: .name → .__name__

    def log_error(self, message):
        self.log(message, level='ERROR')  # Исправлено: lever → level

class UserService(LogMixin):  # Исправлено: UserSevice → UserService
    def create_user(self, name):
        self.log(f'creating user {name}')
        self.log(f'user {name} created')

class OrderService(LogMixin):
    def create_order(self, user_id):
        self.log(f'creating order for user {user_id}')
        self.log(f'order for user {user_id} created')

u = UserService()  # Исправлено: UserSevice → UserService
u.create_user('John')

o = OrderService()
o.create_order(1)




