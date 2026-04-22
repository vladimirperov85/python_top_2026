from sqlalchemy import ForeignKey, Column, Integer, String, Boolean,create_engine,select
from sqlalchemy.orm import DeclarativeBase,Session,declarative_base,Mapped,Mapper,Session,relationship,mapped_column
from datetime import date
from typing import List


class Base(DeclarativeBase):
    pass    

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)

    books: Mapped[List['Book']] = relationship(back_populates='author',)
    
    def __repr__(self):
        return f'<Author(name={self.name}, id={self.id})>'
    

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    title: Mapped[str] = mapped_column(String(100),nullable=False)
    year: Mapped[int] = mapped_column(Integer,nullable=False)
    author: Mapped['Author'] = relationship(back_populates='books')
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    def __repr__(self):
        return f'<Book(title={self.title}, year={self.year}, author_id={self.author_id})>'
    

# if __name__ == '__main__':
#     engine = create_engine('sqlite:///test.db')
#     Base.metadata.create_all(engine)

#     with Session(engine) as session:
        # st  = select(Author).where(Author.name == 'Айзек Азимов')
        # result = session.execute(st).scalar_one_or_none()
        # if result:
        #     print(f'Автор {result.books}')
        # st_book = select(Book).where(Book.title.like('%Основ%'))
        # book_result = session.execute(st_book).scalar_one_or_none()
        # if book_result:
        #     print(f'Книга {book_result}')
        # 
        
        # with Session(engine) as session:
        #     st = select(Book).where(Book.title == 'Основание')
        #     book_del = session.execute(st).scalar_one_or_none()
        #     if book_del:
        #         print(f'Книга {book_del}')
        #         session.delete(book_del)
        #         session.commit()
        #         print('Удалено')




