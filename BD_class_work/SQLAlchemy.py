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

    books: Mapped[List['Book']] = relationship(back_populates='author',cascade='all,delet-orphan')
    
    def __repr__(self):
        return f'<Author(name={self.name}, id={self.id})>'
