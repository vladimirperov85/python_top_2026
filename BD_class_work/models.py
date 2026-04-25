from sqlalchemy import ForeignKey, Column, Integer, String, Boolean,create_engine,select,Numeric
from sqlalchemy.orm import DeclarativeBase,Session,declarative_base,Mapped,Mapper,Session,relationship,mapped_column,selectinload,joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from typing import List,Optional, Sequence
from decimal import Decimal
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass


class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    products: Mapped[List['Product']] = relationship(back_populates='manufacturer',cascade="all, delete-orphan",lazy = 'select')
    def __repr__(self):
        return f'<Manufacturer(name={self.name}, id={self.id})>'
    
    def __str__(self):
        return self.name
    


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturers.id'),nullable=False)
    category: Mapped[str] = mapped_column(String(100),nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    manufacturer: Mapped['Manufacturer'] = relationship(back_populates='products')
    orders: Mapped[List['Order']] = relationship(back_populates='product',lazy = 'select')
    serial_number:Mapped[Optional[str]] = mapped_column(String(100),unique=True,nullable=False)
    def __repr__(self):
        return f'<Product(name={self.name}, category={self.category}, price={self.price}, manufacturer_id={self.manufacturer_id})>'
    
        
    def __str__(self):
        return f'Product {self.name} ({self.category} {self.price})'

class Customer(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100),nullable=False)
    last_name: Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    orders: Mapped[List['Order']] = relationship(back_populates='customer',lazy = 'select')
    def __repr__(self):
        return f'<Customer(first_name={self.first_name}, last_name={self.last_name}, email={self.email}, id={self.id})>'

    def __str__(self):
        return f'Customer {self.first_name} {self.last_name} ({self.email})'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

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
    
    def __str__(self):
        return f'Order {self.id} ({self.status} {self.order_date})'
    
    @property
    def is_active(self):
        active_statuses = {'Progressing','Shipped','Confirmed','Pending'}
        return self.status in active_statuses

class StoreManager:
    
    def __init__(self, db_url: str):
        self.engine = create_engine(f'sqlite:///{db_url}', echo=False, connect_args={'check_same_thread': False})
        Base.metadata.create_all(self.engine) 
        logger.info(f'Connect to DB : {db_url}')  # <- исправлен f-string
    
    def _get_session(self) -> Session:
        return Session(self.engine)
    
    def _fetch_one(self, stmt):  # <- исправлено название
        try:
            with self._get_session() as session:
                result = session.scalar(stmt)
                return result
        except SQLAlchemyError as e:
            logger.error(f'Error request: {e}')
            raise
    
    def _fetch_all(self, stmt):  # <- правильный отступ
        try:
            with self._get_session() as session:
                result = session.scalars(stmt).all()
                return result
        except SQLAlchemyError as e:
            logger.error(f'Errors request: {e}')
            raise
    
    def _save_obj(self, obj_save):  # <- правильный отступ
        try:
            with self._get_session() as session:
                session.add(obj_save)
                session.commit()
                session.refresh(obj_save)
                session.expunge(obj_save)
                return obj_save
        except SQLAlchemyError as e:
            logger.error(f'Error save obj: {e}')
            raise
    
    def delete_obj(self, obj_del):  # <- правильный отступ
        try:
            with self._get_session() as session:
                session.delete(obj_del)
                session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f'Error delete obj: {e}')
            raise
    
    def add_manufacturer(self, name: str) -> Manufacturer:
        manufacturer = Manufacturer(name=name)
        return self._save_obj(manufacturer)  # <- используется _save_obj
    
    def get_manufacturer_by_name(self, name: str) -> Optional[Manufacturer]:
        if not name or not isinstance(name, str):
            raise ValueError('Название не должно быть пустой строкой')
        stmt = select(Manufacturer).where(Manufacturer.name == name.strip())
        return self._fetch_one(stmt)
    
    def get_all_manufacturers(self) -> Sequence[Manufacturer]:
        stmt = select(Manufacturer)
        return self._fetch_all(stmt)
    
    
    def find_manufacturer_by_id(self,manufacturer_id:int)-> Optional[Manufacturer]:
            if not isinstance(manufacturer_id,int) or manufacturer_id <= 0:
                raise ValueError('ID должен быть целым положительным числом')
            stmt = select(Manufacturer).where(Manufacturer.id == manufacturer_id)
            return self._fetch_one(stmt)
    
    def update_manufacturer(self, manufacturer_id: int, new_name: str) -> bool:
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError('Название не должно быть пустой строкой')
        manufacturer = self.find_manufacturer_by_id(manufacturer_id)
        if not manufacturer:
            logger.warning(f'Производитель с ID {manufacturer_id} не найден')
            return False
        old_name = manufacturer.name
        manufacturer.name = new_name.strip()
        self._save_obj(manufacturer)
        logger.info(f'Производитель {old_name} обновлен на {new_name}')
        return True  
    
    