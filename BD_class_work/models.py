from sqlalchemy import ForeignKey, Column, Integer, String, Boolean,create_engine,select
from sqlalchemy.orm import DeclarativeBase,Session,declarative_base,Mapped,Mapper,Session,relationship,mapped_column
from datetime import date
from typing import List,Optional

class Base(DeclarativeBase):
    pass

class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    products: Mapped[List['Product']] = relationship(back_populates='manufacturer',cascade="all, delete-orphan")
    def __repr__(self):
        return f'<Manufacturer(name={self.name}, id={self.id})>'

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturers.id'),nullable=False)
    category: Mapped[str] = mapped_column(String(100),nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    manufacturer: Mapped['Manufacturer'] = relationship(back_populates='products')
    orders: Mapped[List['Order']] = relationship(back_populates='product')
    def __repr__(self):
        return f'<Product(name={self.name}, category={self.category}, price={self.price}, manufacturer_id={self.manufacturer_id})>'


class Customer(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100),nullable=False)
    last_name: Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    orders: Mapped[List['Order']] = relationship(back_populates='customer',cascade="all, delete-orphan")
    def __repr__(self):
        return f'<Customer(first_name={self.first_name}, last_name={self.last_name}, email={self.email}, id={self.id})>'

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'),nullable=False)
    product: Mapped['Product'] = relationship(back_populates='orders')
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'),nullable=False)
    customer: Mapped['Customer'] = relationship(back_populates='orders')
    order_date: Mapped[date] = mapped_column(nullable=False)
    delivery_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(200),nullable=False)

    def __repr__(self):
        return f'<Order(product_id={self.product_id}, customer_id={self.customer_id}, order_date={self.order_date}, delivery_date={self.delivery_date}, status={self.status})>'
    

class StoreManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(f'sqlite:///{db_url}',echo=False)
        Base.metadata.create_all(self.engine)  

    def _execute_query(self, stmt):
        with Session(self.engine) as session:
            result = session.execute(stmt)
            # Определяем тип запроса
            if stmt.is_select:
                # Для SELECT запросов
                if hasattr(stmt, '_limit_clause') or 'WHERE' in str(stmt).upper():
                    # Может быть один результат
                    return result.scalar_one_or_none()
                return result.scalars().all()
            return result
            
    def _execute_mutation(self,obj_save):
        with Session(self.engine) as session:
            session.add(obj_save)
            session.commit()

        
    
    def add_manufacturer(self,name: str)-> Manufacturer:
        manufacturer = Manufacturer(name = name)
        self._execute_mutation(manufacturer)
        print(f'Производитель {name} добавлен')
        return manufacturer

            



