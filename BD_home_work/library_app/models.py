from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

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


class BookIssue(Base):
    __tablename__ = "book_issues"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"BookIssue(id={self.id}, book_id={self.book_id}, reader_id={self.reader_id}, issue_date={self.issue_date})"


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

    def add_book(self, title, author_id, year, isbn=None):
        try:
            if not self.find_author_by_id(author_id):
                print(f"Автор с ID {author_id} не найден.")
                return None
            book = Book(title=title, author_id=author_id, year=year, isbn=isbn)
            self.session.add(book)
            self.session.commit()
            print(f"Книга {title} добавлена в базу данных.")
            return book
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при добавлении читателя: {e}")
            raise

    def get_all_authors(self):
        return self.session.query(Author).all()

    def get_all_books(self):
        return self.session.query(Book).all()

    def find_author_by_id(self, author_id):
        return self.session.query(Author).filter(Author.id == author_id).first()

    def find_book_by_id(self, book_id):
        return self.session.query(Book).filter(Book.id == book_id).first()

    def update_author(self, author_id, new_name):
        author = self.session.query(Author).filter_by(id=author_id).first()
        if author:
            author.name = new_name
            self.session.commit()
            print(f"Имя автора с ID {author_id} обновлено на '{new_name}'.")
        else:
            print(f"Автор с ID {author_id} не найден.")

    def update_book(self, book_id, new_title=None, new_year=None, new_isbn=None):
        book = self.find_book_by_id(book_id)
        if book:
            if new_title is not None:
                book.title = new_title
            if new_year is not None:
                book.year = new_year
            if new_isbn is not None:
                book.isbn = new_isbn
            self.session.commit()
            print(f"Книга с ID {book_id} обновлена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def delete_author(self, author_id):
        author = self.session.query(Author).filter_by(id=author_id).first()
        if not author:
            print(f"Автор с ID {author_id} не найден.")
            # IDE может не видеть .books — это нормально, добавлено через relationship()
        if author.books:
            raise ValueError("у автора есть книги а базе данных.Удаление невозможно")
        self.session.delete(author)
        self.session.commit()
        print(f"Автор с ID {author_id} удален из базы данных.")

    def delete_book(self, book_id):
        book = self.find_book_by_id(book_id)
        if not book:
            raise ValueError(f"Книга с ID {book_id} не найдена.")
        book_issue = self.is_book_issued(book.id)
        if book_issue:
            raise ValueError(
                f"Книга с {book_id} имеет активные записи. Удаление невозможно"
            )
        self.session.delete(book)
        self.session.commit()
        print(f"Книга с ID {book_id} удалена из базы данных.")

    def add_reader(self, first_name, last_name, email):
        try:
            reader = Reader(first_name=first_name, last_name=last_name, email=email)
            self.session.add(reader)
            self.session.commit()
            print(f"Читатель {first_name} добавлен в базу данных.")
            return reader
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при добавлении читателя: {e}")
            raise

    def get_all_readers(self):
        return self.session.query(Reader).all()

    def find_reader_by_id(self, reader_id):
        return self.session.query(Reader).filter(Reader.id == reader_id).first()

    def update_reader(
        self, reader_id, new_first_name=None, new_last_name=None, new_email=None
    ):
        reader = self.find_reader_by_id(reader_id)
        if reader:
            if new_first_name is not None:
                reader.first_name = new_first_name
                print(f"Имя читателя с ID {reader_id} обновлено на '{new_first_name}'.")
            if new_last_name is not None:
                reader.last_name = new_last_name
                print(f"Имя читателя с ID {reader_id} обновлено на '{new_last_name}'.")
            if new_email is not None:
                reader.email = new_email
                print(f"Имя читателя с ID {reader_id} обновлено на '{new_email}'.")
            self.session.commit()
        else:
            print(f"Читатель с ID {reader_id} не найден.")

    def delete_reader(self, reader_id):
        reader = self.find_reader_by_id(reader_id)
        if not reader:
            print(f"Читатель с ID {reader_id} не найден.")
            return
        active_issues = (
            self.session.query(BookIssue)
            .filter(BookIssue.reader_id == reader_id, BookIssue.return_date.is_(None))
            .first()
        )
        if active_issues:
            raise ValueError(
                f"Читатель с ID {reader_id} имеет активные выдачи. Удаление невозможно"
            )
        self.session.delete(reader)
        self.session.commit()
        print(f"Читатель с ID {reader_id} удален из базы данных.")

    def is_book_issued(self, book_id):
        active_issue = (
            self.session.query(BookIssue)
            .filter(BookIssue.book_id == book_id, BookIssue.return_date.is_(None))
            .first()
        )
        return active_issue is not None

    def issue_book_to_reader(self, book_id, reader_id):
        if self.is_book_issued(book_id):
            print(f"Книга с ID {book_id} уже выдана.")
            return None
        book = self.find_book_by_id(book_id)
        if not book:
            print(f"Книга с ID {book_id} не найдена.")
            return None
        reader = self.find_reader_by_id(reader_id)
        if not reader:
            print(f"Читатель с ID {reader_id} не найден.")
            return None
        issue = BookIssue(book_id=book_id, reader_id=reader_id, issue_date=date.today())
        self.session.add(issue)
        self.session.commit()
        print(
            f"Книга {book.title} выдана читателю {reader.first_name} {reader.last_name} {date.today()}."
        )
        return issue

    def return_book_from_reader(self, issue_id):
        issue = self.session.query(BookIssue).filter(BookIssue.id == issue_id).first()
        if not issue:
            print(f"Выдача с ID {issue_id} не найдена.")
            return None
        if issue.return_date is not None:
            print(f"Книга с ID {issue.book_id} уже возвращена.")
        else:
            issue.return_date = date.today()
            self.session.commit()
            print(f"Книга с ID {issue.book_id} возвращена {date.today()}")
            return issue

    def get_active_issues(self):
        active_issues = (
            self.session.query(BookIssue).filter(BookIssue.return_date.is_(None)).all()
        )
        if len(active_issues) == 0:
            print("Нет активных выдач.")
        else:
            print(f"Найдено активных выдач:{len(active_issues)}")
        return active_issues

    def find_books_by_author_name(self, author_name):
        books = (
            self.session.query(Book)
            .join(Author)
            .filter(Author.name == author_name)
            .all()
        )
        return books

    def display_all_books_with_authors(self):
        books = self.session.query(Book).join(Author).all()
        for book in books:
            print(f'Книга: "{book.title}" - автор: {book.author.name}')
