# создание класса car
class Car:
    def __init__(self,brand,model,year,is_available_sale =True):
        self.brand = brand
        self.model = model
        self.year = year
        self.is_available_sale = is_available_sale
        self.is_power = False
        self.is_drive = False

        # определим отрибут обьекта без передчи в конструктор

        self.car_type = 'passenger car'

    def get_info(self):
        print(f'Марка:{self.brand} {self.model} {self.year}')

    def power_on(self):
        if not self.is_power:
            print(f'Автомобиль {self.brand} {self.model} {self.year} года заведен')
            self.is_power = True
        else:
            print(f'Автомобиль уже заведен')

    def power_off(self):
        if self.is_power:
            self.is_power = False
            print(f'Автомобиль {self.brand} {self.model} {self.year} года заглушен!')
        else:
            print(f'Автомобиль {self.brand} {self.model} {self.year} уже заглушен!')

    def car_go(self):
        self.is_drive = True
        print(f'Автомобиль {self.brand} {self.model} {self.year} года поехал!')

    def car_stop(self):
        if self.is_power:
            print(f'Автомобиль {self.brand} {self.model} {self.year} автомобиль нельзя заглушить он в движении')
        else:
            print('Автомобиль  остновлен!!!')

    def car_turn(self,direction):
        if direction == 'left'or direction == 'right':
            print(f'Автомобиль {self.brand} {self.model} {self.year} повернул на {direction}')
        else:
            print(f'Ошибка: "{direction}" - это неверное направление.')
            # или просто вернуть None, но без принта выше







car_1 = Car(brand='Lada',model = 'Vesta',year = 2025)
car_2 = Car(brand='BMV',model = 'M3',year = 2021,is_available_sale = False)
car_1.power_on()
car_1.car_go()
car_1.car_stop()
car_1.car_stop()
car_1.power_off()
car_1.car_stop()


