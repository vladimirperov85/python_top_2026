from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine('sqlite:///products.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)  # ← исправлено: was is_avalable

    def __repr__(self):
        return f'<Product(name={self.name}, price={self.price}, stock={self.stock})>'


class ProductManager:  # ← исправлено: стиль названия класса (PEP8)
    def __init__(self):
        pass

    def _create(self, name, price, stock=0, is_available=True):
        session = Session()
        try:
            product = Product(
                name=name,
                price=price,
                stock=stock,
                is_available=is_available  # ← исправлено
            )
            session.add(product)
            session.commit()
            print(f'Товар {name} добавлен в базу данных id={product.id}')
            return product
        except Exception as e:
            session.rollback()
            print(f'Ошибка при добавлении товара: {e}')
            return None
        finally:
            session.close()

    def get_all(self):
        session = Session()
        products = session.query(Product).all()
        session.close()
        return products

    def get_by_id(self, product_id):
        session = Session()
        product = session.query(Product).filter(Product.id == product_id).first()
        session.close()
        return product

    def get_by_name(self, name):
        session = Session()
        product = session.query(Product).filter(Product.name == name).first()
        session.close()
        return product

    def get_by_available(self, is_available):
        session = Session()
        products = session.query(Product).filter(Product.is_available == is_available).all()
        session.close()
        return products

    def get_by_stock(self, stock):
        session = Session()
        products = session.query(Product).filter(Product.stock == stock).all()  # ← исправлено: было == 0
        session.close()
        return products

    def get_by_price(self, min_price, max_price):
        session = Session()
        products = session.query(Product).filter(
            Product.price >= min_price,
            Product.price <= max_price  # ← исправлено: раньше было <= min_price
        ).all()
        session.close()
        return products

    def update_price(self, product_id, new_price):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                old_price = product.price
                product.price = new_price
                session.commit()
                print(f'Цена товара {product.name} изменена с {old_price} на {new_price}')
                return True
            else:
                print(f'Товар с id {product_id} не найден')
                return False
        except Exception as e:
            session.rollback()
            print(f'Ошибка при изменении цены: {e}')
            return False
        finally:
            session.close()

    def update_stock(self, product_id, new_stock):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                old_stock = product.stock
                product.stock = new_stock
                session.commit()
                print(f'Количество товара {product.name} изменено с {old_stock} на {new_stock}')
                return True
            else:
                print(f'Товар с id {product_id} не найден')
                return False
        except Exception as e:
            session.rollback()
            print(f'Ошибка при изменении количества: {e}')
            return False
        finally:
            session.close()

    def add_stock(self, product_id, quantity):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if not product:
                print(f'Товар с id {product_id} не найден')
                return False
            if quantity > 0:
                product.stock += quantity
                session.commit()
                print(f'Количество товара {product.name} увеличилось на {quantity}, всего {product.stock}')
                return True
            else:
                print('Количество товара должно быть положительным')  # ← исправлено: опечатка
                return False
        except Exception as e:
            session.rollback()
            print(f'Ошибка при добавлении количества: {e}')
            return False
        finally:
            session.close()

    def update_available(self, product_id, is_available):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                product.is_available = is_available  # ← исправлено
                status = 'Доступно' if is_available else 'Недоступно'
                session.commit()
                print(f'Товар {product.name} теперь {status}')
                return True
            else:
                print(f'Товар с id {product_id} не найден')
                return False
        except Exception as e:
            session.rollback()
            print(f'Ошибка при обновлении доступности: {e}')
            return False
        finally:
            session.close()

    def update(self, product_id, **kwargs):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                for key, value in kwargs.items():
                    if hasattr(product, key):
                        setattr(product, key, value)
                session.commit()
                print(f'Товар {product.name} обновлен')
                return True
            else:
                print(f'Товар с id {product_id} не найден')
                return False
        except Exception as e:
            session.rollback()
            print(f'Ошибка при обновлении товара: {e}')
            return False
        finally:
            session.close()

    def delete_by_name(self, product_id):
        session = Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                session.delete(product)
                session.commit()
                print(f'Товар {product.name} удален')
                return True
            else:
                print(f'Товар с id {product_id} не найден')
                return False
        except Exception as e:
            session.rollback()
            print(f'Ошибка при удалении товара: {e}')
            return False
        finally:
            session.close()


class ProductViewer:

    def print_header(self,text):
        print(f'===={text}======')

    def print_one(self, product):
        if product:
            status = 'В наличие' if product.is_available else 'Нет в наличии'
            stock_info = f'{product.stock} шт. в наличии' if product.stock > 0 else '0 шт'
            print(f'id{product.id} | {product.name} | {product.price} | {stock_info} | {status}')
        else:
            print('Товар не найден')

    def print_all(self, products):
        if  not products:
            print('Товары не найдены')
        for product in products:
            self.print_one(product)

    def print_statistics(self, products):
        if not products:
            print('Не найдены')
            return
        total = len(products)
        available = sum(1 for p in products if p.is_available)
        in_stock = sum(p.stock for p in products if p.stock > 0)
        total_price = sum(p.price * p.stock for p in products)
        avg_price = sum(p.price for p in products) / total 
        
        print(f'Всего товаров {total}')
        print(f'Доступно {available}')  
        print(f'В наличии {in_stock}')
        print(f'Общая стоимость {total_price}')
        print(f'Средняя цена {avg_price}')



if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    # print("Таблицы созданы (если не существовали).")
    manager = ProductManager()
    viewer = ProductViewer()

    # viewer.print_header('База готова')

    # manager._create('Ноутбук', 100000, 14)
    # manager._create('Мышь', 4000, 5)
    # manager._create('Клавиатура', 30000, 7)
    # manager._create('Монитор', 20000, 4)
    # manager._create('Системный блок', 500000, 8)
    # manager._create('Наушники', 25000, 11)
    # manager._create('Роутер', 60000, 23)
    # manager._create('Телефон', 870000, 10)

    # print('Обновление товара')
    # manager.update(1, name='Ноутбук Lenovo', price=120000, stock=10, is_available=False)
    # print('Проверка')
    # products = manager.get_all()
    # viewer.print_all(products)

    # by_price = manager.get_by_price(10000, 100000)
    # viewer.print_all(by_price)

    # print('Удаление')
    # manager.delete_by_name(product_id = 2)

    products = manager.get_all()
    # viewer.print_all(products)
    print('Статистика')
    viewer.print_statistics(products)

