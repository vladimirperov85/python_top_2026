from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    Boolean,
    create_engine,
    select,
    Numeric,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from typing import List, Optional, cast, TypeVar
from decimal import Decimal
import logging

_T = TypeVar("_T")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True
)

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    products: Mapped[List["Product"]] = relationship(
        back_populates="manufacturer", cascade="all, delete-orphan", lazy="select"
    )

    def __repr__(self):
        return f"<Manufacturer(name={self.name}, id={self.id})>"

    def __str__(self):
        return self.name


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturers.id"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="products")
    orders: Mapped[List["Order"]] = relationship(
        back_populates="product", lazy="select"
    )
    serial_number: Mapped[Optional[str]] = mapped_column(
        String(100), unique=True, nullable=False
    )

    def __repr__(self):
        return f"<Product(name={self.name}, category={self.category}, price={self.price}, manufacturer_id={self.manufacturer_id})>"

    def __str__(self):
        return f"Product {self.name} ({self.category} {self.price})"


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    orders: Mapped[List["Order"]] = relationship(
        back_populates="customer", lazy="select"
    )

    def __repr__(self):
        return f"<Customer(first_name={self.first_name}, last_name={self.last_name}, email={self.email}, id={self.id})>"

    def __str__(self):
        return f"Customer {self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped["Product"] = relationship(back_populates="orders")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    order_date: Mapped[date] = mapped_column(nullable=False)
    delivery_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(200), nullable=False)

    def __repr__(self):
        return f"<Order(product_id={self.product_id}, customer_id={self.customer_id}, order_date={self.order_date}, delivery_date={self.delivery_date}, status={self.status})>"

    def __str__(self):
        return f"Order {self.id} ({self.status} {self.order_date})"

    @property
    def is_active(self):
        active_statuses = {"Progressing", "Shipped", "Confirmed", "Pending"}
        return self.status in active_statuses


class StoreManager:
    STATUS_PROGRESSING = "Progressing"
    STATUS_SHIPPED = "Shipped"
    STATUS_DELIVERED = "Delivered"
    STATUS_CANCELED = "Canceled"

    ACTIVE_STATUSES = {STATUS_PROGRESSING, STATUS_SHIPPED, "Confirmed", "Pending"}

    def __init__(self, db_url: str):
        self.engine = create_engine(
            f"sqlite:///{db_url}", echo=False, connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(self.engine)
        logger.info(f"Connect to DB : {db_url}")

    def _get_session(self) -> Session:
        return Session(self.engine)

    def _fetch_one(self, stmt) -> Optional[_T]:
        try:
            with self._get_session() as session:
                result = session.scalar(stmt)
                return result
        except SQLAlchemyError as e:
            logger.error(f"Error request: {e}")
            raise

    def _fetch_all(self, stmt) -> List[_T]:
        try:
            with self._get_session() as session:
                result = session.scalars(stmt).all()
                return list(result)
        except SQLAlchemyError as e:
            logger.error(f"Errors request: {e}")
            raise

    def _save_obj(self, obj_save: _T) -> _T:  # Исправлено: отступы
        try:
            with self._get_session() as session:
                session.add(obj_save)
                session.commit()
                session.refresh(obj_save)
                session.expunge(obj_save)
                return obj_save
        except SQLAlchemyError as e:
            logger.error(f"Error save obj: {e}")
            raise

    def _delete_obj(self, obj_del) -> bool:
        try:
            with self._get_session() as session:
                session.delete(obj_del)
                session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error delete obj: {e}")
            return False

    def _execute_query(self, stmt):
        with Session(self.engine) as session:
            result = session.execute(stmt)
            # Определяем тип запроса
            if stmt.is_select:
                # Для SELECT запросов
                if hasattr(stmt, "_limit_clause") or "WHERE" in str(stmt).upper():
                    # Может быть один результат
                    return result.scalar_one_or_none()
                return result.scalars().all()
            return result

    def add_manufacturer(
        self, name: str
    ) -> Manufacturer:  # Исправлено: было get_manufacturer с дублированием
        if not isinstance(name, str):
            raise ValueError("Название должно быть строкой")
        if not name.strip():
            raise ValueError("Название не должно быть пустой строкой")
        manufacturer = Manufacturer(name=name.strip())
        saved_manufacturer = self._save_obj(
            manufacturer
        )  # Исправлено: было save_obj, нужно _save_obj
        logger.info(f"Производитель {saved_manufacturer.name} добавлен")
        return saved_manufacturer

    def get_manufacturers(
        self, stmt=None
    ) -> List[Manufacturer]:  # Исправлено: было дублирование имени метода
        if stmt is None:
            stmt = select(Manufacturer)
        return self._fetch_all(stmt)

    def find_manufacturer_by_id(self, manufacturer_id: int) -> Optional[Manufacturer]:
        if not isinstance(manufacturer_id, int) or manufacturer_id <= 0:
            raise ValueError("ID должен быть целым положительным числом")
        stmt = select(Manufacturer).where(Manufacturer.id == manufacturer_id)
        return self._fetch_one(stmt)

    def update_manufacturer(self, manufacturer_id: int, new_name: str) -> bool:
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Название не должно быть пустой строкой")
        manufacturer = self.find_manufacturer_by_id(manufacturer_id)
        if not manufacturer:
            logger.warning(f"Производитель с ID {manufacturer_id} не найден")
            return False
        old_name = manufacturer.name
        manufacturer.name = new_name.strip()
        self._save_obj(manufacturer)  # Исправлено: было save_obj, нужно _save_obj
        logger.info(f"Производитель {old_name} обновлен на {new_name}")
        return True

    def delete_manufacturer(self, manufacturer_id: int) -> bool:
        manufacturer = self.find_manufacturer_by_id(manufacturer_id)
        if not manufacturer:
            logger.warning(f"Производитель с ID {manufacturer_id} не найден")
            return False
        if manufacturer.products:
            logger.warning(
                f"Производитель {manufacturer.id} имеет товары, удаление невозможно, так как есть {len(manufacturer.products)} товаров"
            )
            return False
        self._delete_obj(manufacturer)  # Исправлено: было _delete_obj, теперь правильно
        logger.info(f"Производитель {manufacturer_id} удален")
        return True

    def add_product(
        self,
        name: str,
        manufacturer_id: int,
        category: str,
        price: Decimal | float | int,
        serial_number: Optional[str] = None,
    ) -> Product:
        if not isinstance(name, str):
            raise ValueError("Название должно быть  строкой")
        if not isinstance(category, str):
            raise ValueError("Название должно быть  строкой")
        if not isinstance(price, (int, float)):
            price = Decimal(str(price))
        elif not isinstance(price, Decimal):
            raise ValueError("Цена должна быть  числом")
        manufacturer = self.find_manufacturer_by_id(manufacturer_id)
        if not manufacturer:
            raise ValueError(f"Производитель с ID {manufacturer_id} не найден")
        product = Product(
            name=name.strip(),
            manufacturer_id=manufacturer_id,
            category=category,
            price=price,
            serial_number=serial_number.strip() if serial_number else None,
        )
        try:
            saved_product = self._save_obj(product)
            logger.info(f"Товар добавлен {saved_product.name}")
            return saved_product
        except SQLAlchemyError as e:
            if "unique constraint failed" in str(e).lower():
                raise ValueError(
                    f"Товар с таким серийным номером {serial_number} уже существует"
                )
            raise

    def find_all_products(self):
        stmt = select(Product)
        return self._fetch_all(stmt)

    def find_product_by_id(self, product_id: int) -> Optional[Product]:
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError(
                "ID должно быть целым положительным числом"
            )  # исправлено сообщение

        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.manufacturer), selectinload(Product.orders))
        )
        return self._fetch_one(stmt)

    def find_products_by_name_or_category(self, query: str) -> List[Product]:
        if not isinstance(query, str) or not query.strip():
            return []
        stmt = select(Product).where(
            Product.name.ilike(f"%{query.strip()}%")
            | Product.category.ilike(f"%{query.strip()}%")
        )
        return self._fetch_all(stmt)

    def update_product(
        self,
        product_id: int,
        new_name: Optional[str] = None,
        new_price: Decimal | float | int | None = None,
        new_serial_number: Optional[str] = None,
    ) -> bool:

        product = self.find_product_by_id(product_id)
        if not product:
            logger.warning(f"Товар с ID {product_id} не найден")
            return False
        if new_name is not None:
            if not isinstance(new_name, str) or not new_name.strip():
                raise ValueError("Название должно быть строкой и не пустой")
            product.name = new_name.strip()
        if new_price is not None:
            if isinstance(new_price, (int, float)):
                new_price = Decimal(str(new_price))
            elif not isinstance(new_price, Decimal):
                raise ValueError("Цена должна быть числом")
            product.price = new_price
        if new_serial_number is not None:
            if not isinstance(new_serial_number, str):
                raise ValueError("Номер серийный должен быть строкой")
            product.serial_number = (
                new_serial_number.strip() if new_serial_number else None
            )
        try:
            self._save_obj(product)
            logger.info(f"Товар с id {product_id} сохранен")
            return True
        except SQLAlchemyError as e:
            if "unique constraint failed" in str(e).lower():
                raise ValueError(
                    f"Товар с таким серийным номером {new_serial_number} уже существует"
                )
            return False

    def delete_product(self, product_id: int) -> bool:
        product = self.find_product_by_id(product_id)
        if not product:
            logger.warning(f"Товар с ID {product_id} не найден")
            return False
        active_orders = [order for order in product.orders if order.is_active]
        if active_orders:
            logger.warning(
                f"Товар {product.name} имеет активные заказы, удаление невозможно",
                f"Он содержится в {len(active_orders)} заказа ",
            )
            return False
        self._delete_obj(product)
        logger.info(f"Товар с id {product_id} удален")
        return True
