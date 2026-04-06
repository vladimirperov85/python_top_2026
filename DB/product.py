from sqlalchemy import create_engine,Column,Integer,String,Boolean,Float
from sqlalchemy.orm import declarative_base,sessionmaker

engine = create_engine('sqlite:///products.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer,primary_key=True)
    name = Column(String(100),nullable=False)
    price  = Column(Float,nullable=False)
    stock = Column(Integer,default=0)
    is_avalable = Column(Boolean,default=True)

    def __repr__(self):
        return f'<Product(name = {self.name},price = {self.price},stock = {self.stock})>'
    
class Productmanager:
    def __init__(self):
        pass

    def _create(self,name,price,stock = 0,is_avalable = True):
        session = Session()

        try:
            product = Product(
                                name = name,
                                price = price,
                                stock = stock,
                                is_avalable = is_avalable

                              )
            session.add(product)
            session.commit()
            print(f'Товар {name} добавлен в базу данных id ={product.id}')
            return product
        except Exception as e:
            session.rollback()
            print(f'Ошибка')
            return None
        finally:
            session.close()

    def get_all(self):
        session = Session()
        products = session.query(Product).all()
        session.close()
        return products
    
    def get_by_id(self,product_id):
        session = Session()
        product = session.query(Product).filter(Product.id == product_id).first()
        session.close()
        return product
    
    def get_by_name(self,name):
        session = Session()
        product = session.query(Product).filter(Product.name == name).first()
        session.close()
        return product

    def get_by_available(self,is_available):
        session = Session()
        products = session.query(Product).filter(Product.is_available == True).all()
        session.close()
        return products
    
    def get_by_stock(self,stock):
        session = Session()
        products = session.query(Product).filter(Product.stock == 0).all()
        session.close()
        return products
    def get_by_price(self,min_price,max_price):
        session = Session()
        products = session.query(Product).filter(Product.price >= min_price,Product.price <= min_price).all()
        session.close()
        return products
    
    def update_price(self,product_id,new_price):
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
            print(f'Ошибка: {e}')
            return False
        finally:
            session.close()


    def update_stock(self,product_id,new_stock):
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
            print(f'Ошибка: {e}')
            return False
        finally:
            session.close()


    
