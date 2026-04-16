from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine

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

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        print(
            "✅ Все таблицы (authors, books, readers) успешно созданы или уже существуют."
        )
