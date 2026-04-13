

from sqlalchemy import create_engine, Column, Integer, String, Boolean,Float
from sqlalchemy.orm import declarative_base, sessionmaker
# подключение к БД
 # только один раз

# базовый класс
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)  
    name = Column(String(100), nullable=False)  # исправлено: String вместо Integer
    email = Column(String(100), unique=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'<user(name = {self.name}, email = {self.email})>'
    
    def is_adult(self):
        return self.age >= 18 if self.age else False

engine = create_engine('sqlite:///mydb.db', echo=True)
# создание таблиц
Base.metadata.create_all(engine)

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float,nullable=False)
    stock = Column(Integer,default=0)
    is_available = Column(Boolean,default=True)
    
    def __repr__(self):
        return f'<product(name = {self.name}, price = {self.price})>'
    
    def in_stock(self):
        return self.stock > 0 and self.is_available 
    
    def add_stock(self, quantity):
        if quantity > 0:
            self.stock += quantity
        else:
            raise ValueError('Количество не должно быть отрицательным')
# Session = sessionmaker(bind=engine)
# session = Session()        
# user1 = User(name='John', email='john@example.com', age=30)
# user2 = User(name='Alice', email='alice@example.com', age=25)

# session.add(user1)
# session.add(user2)

# session.commit()

# print(f'Пользователи {user1.id} и {user2.id} добавлены в БД')
# session.close()

# first_user = session.query(User).first()
# print(first_user)

# user = session.query(User).get('')
# print(user)

# ault_user = session.query(User).filter(User.age >= 18).all()
# print(f'{len(ault_user)} пользователей старше 18 лет')




