# Определение класса Animal
class Animal:
    counter = 0
    def __init__(self,breed,name,color = 'grey'):
        self.breed = breed
        self.name = name
        self.color = color
        self.country = 'Russia'
        Animal.counter += 1


    def hello(self):
        print(f'Hello, I am {self.breed} {self.name},i am {self.vozrast}')

    def bye(self,friend):
        print(f'Bye, {friend}.{self.name} go to sleep!')
print(Animal.counter)
dog_chappy = Animal("spaniel","Chappy")
print(dog_chappy.counter)


