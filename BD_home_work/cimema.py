from sqlalchemy import create_engine, Column, Integer, String,Float,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///C:/Users/PC/Desktop/WINDOWS(ДОМАШНИЙ РЕПОЗИТОРИЙ)/BD_home_work/My_bd.db')

Base = declarative_base()



class Movie(Base):

    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    genre = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    duration = Column(Integer)
    is_available = Column(Boolean,default=True)
    
    
    
    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}', genre='{self.genre}', year={self.year}, rating={self.rating}, available={self.is_available})>"
    
    

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_movie( session, title, genre, year,duration,rating):
    movie = Movie(title=title, genre=genre, year=year, duration=duration,rating=rating)
    session.add(movie)
    session.commit()
    print(f'Фильм {title} добавлен в базу данных!>')

    

def get_all_movies():
    return session.query(Movie).all()

def get_movies_by_genre(genre_name):
    return session.query(Movie).filter(Movie.genre == genre_name).all()

def get_high_rated_movies(min_rating):
    return session.query(Movie).filter(Movie.rating >= min_rating).all()

def get_movies_after_year(year):
    return session.query(Movie).filter(Movie.year > year).all()

def get_movie_by_title(title):
    return session.query(Movie).filter(Movie.title == title).first()


if __name__ == "__main__":
    # Можно закоментировать добавление фильмов после первого запуска скрипта. что бы не были созданы дубликаты при повторном 
    # запуске скрипта
    # create_movie(session,"Побег из Шоушенка", "Драма", 1994, 142, 9.3)
    # create_movie(session,"Крестный отец", "Драма", 1972, 175, 9.2)
    # create_movie(session,"Темный рыцарь", "Боевик", 2008, 152, 9.0)
    # create_movie(session,"Криминальное чтиво", "Криминал", 1994, 154, 8.9)
    # create_movie(session,"Властелин колец", "Фэнтези", 2001, 178, 8.8)
    
    
    print('----------------------------------------')
    print('----------------------------------------')
    print("Вывод всех фильмов из таблицы 'movies' ")
    print(get_all_movies())
    print('----------------------------------------')
    
    print("Вывод всех фильмов из таблицы по названию жанра ")
    print(get_movies_by_genre("Драма"))
    print('----------------------------------------')
    
    print("Вывод фильмов с рейтингом больше или равным 9.0")
    print(get_high_rated_movies(9.0))
    print('-----------------------------------------')
    
    print("Вывод фильмов после 2000-го года")
    print(get_movies_after_year(2000))
    print('----------------------------------------')
    
    print("Вывод фильма по названию")
    print(get_movie_by_title("Темный рыцарь"))

    
    session.close()