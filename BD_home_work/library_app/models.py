from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="author", cascade="all,delete-orphan")

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    year = Column(Integer)
    isbn = Column(String, unique=True)

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title}, author_id={self.author_id}, year={self.year}, isbn={self.isbn})"


class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"Reader(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})"


class LibraryManager:

    def __init__(self, database_url="sqlite:///database.db"):
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.session = self.SessionLocal()

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        print("Таблицы созданы или уже существуют.")

    def add_author(self, name):
        author = Author(name=name)
        self.session.add(author)
        self.session.commit()
        print(f"Автор {name} добавлен в базу данных.")
        return author

    def add_book(self,title, author_id, year, isbn):
        book = Book(title=title, author_id=author_id, year=year, isbn=isbn)
        self.session.add(book)
        self.session.commit()
        print(f"Книга {title} добавлена в базу данных.")
        return book

    def get_all_authors(self):
        return self.session.query(Author).all()

    def find_author_by_id(self, author_id):
        return self.session.query(Author).filter(Author.id == author_id).first()

    def update_author(self, author_id, new_name):
        author = self.session.query(Author).filter_by(id=author_id).first()
        if author:
            author.name = new_name
            self.session.commit()
            print(f"Имя автора с ID {author_id} обновлено на '{new_name}'.")
        else:
            print(f"Автор с ID {author_id} не найден.")

    def delete_author(self, author_id):
        author = self.session.query(Author).filter_by(id=author_id).first()
        if author:
            self.session.delete(author)
            self.session.commit()
            print(f"Автор с ID {author_id} удален из базы данных.")
        else:
            print(f"Автор с ID {author_id} не найден.")
