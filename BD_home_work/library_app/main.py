from sqlalchemy.orm import sessionmaker
from models import Base, Author, Book, Reader, LibraryManager


manager = LibraryManager("sqlite:///BD_home_work/My_bd.db")
manager.create_tables()

Session = sessionmaker(bind=manager.engine)
session = Session()

if __name__ == "__main__":
    pass
