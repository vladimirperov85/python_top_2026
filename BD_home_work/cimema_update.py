from turtle import update
from venv import create

from sqlalchemy import (
    all_,
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    false,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///C:/Users/PC/Desktop/WINDOWS(HOME REPOZITORY)/BD_home_work/My_bd.db",
    echo=False,
)

Base = declarative_base()


class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    duration = Column(Integer)
    is_available = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}', genre='{self.genre}', year={self.year}, rating={self.rating}, available={self.is_available})>"


class MovieManager:

    def __init__(self, engine):
        self.engine = engine
        Base.metadata.create_all(engine)

    def create_movie(self, title, genre, year, duration, rating):
        new_movie = Movie(
            title=title, genre=genre, year=year, duration=duration, rating=rating
        )
        session = sessionmaker(bind=self.engine)()
        session.add(new_movie)
        session.commit()
        session.refresh(new_movie)
        session.close()
        print(f"Фильм {title} добавлен в базу данных id ={new_movie.id}")
        return new_movie

    def get_all_movies(self):
        session = sessionmaker(bind=self.engine)()
        movies = session.query(Movie).all()
        session.close()
        return movies

    def get_by_id(self, movie_id):
        session = sessionmaker(bind=self.engine)()
        movie = session.query(Movie).filter(Movie.id == movie_id).first()
        session.close()
        return movie

    def get_movies_by_genre(self, genre):
        session = sessionmaker(bind=self.engine)()
        movies = session.query(Movie).filter(Movie.genre == genre).all()
        session.close()
        return movies

    def get_movies_by_year(self, year):
        session = sessionmaker(bind=self.engine)()
        movies = session.query(Movie).filter(Movie.year > year).all()
        session.close()
        return movies

    def get_high_rated_movies(self, rating):
        session = sessionmaker(bind=self.engine)()
        movies = session.query(Movie).filter(Movie.rating >= rating).all()
        session.close()
        return movies

    def update_full(self, movie_id, **kwargs):
        session = sessionmaker(bind=self.engine)()
        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if movie:
                for key, value in kwargs.items():
                    setattr(movie, key, value)
                session.commit()
                session.refresh(movie)
                print(f"Фильм с id={movie_id} успешно обновлен")
                return movie
            else:
                print(f"Фильм с id={movie_id} не найден")
                return None
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении фильма: {e}")
            return None
        finally:
            session.close()

    def get_movie_by_title(self, title):
        with sessionmaker(bind=self.engine)() as session:
            try:
                movie = session.query(Movie).filter(Movie.title == title).first()
                if movie is None:
                    print(f"Фильм '{title}' не найден!")
                    return None
                return movie
            except Exception as e:
                print(f"Ошибка при поиске фильма по названию: {e}")
                return None

    def update_rating(self, movie_id, new_rating):
        session = sessionmaker(bind=self.engine)()
        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if movie:
                movie.rating = new_rating
                session.commit()
                session.refresh(movie)
                print(
                    f"Рейтинг фильма с id={movie_id} успешно обновлен до {new_rating}"
                )
                return movie
            else:
                print(f"Фильм с id={movie_id} не найден")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении рейтинга: {e}")
        finally:
            session.close()

    def update_genre(self, movie_id, new_genre):
        session = sessionmaker(bind=self.engine)()
        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if movie:
                movie.genre = new_genre
                session.commit()
                session.refresh(movie)
                print(f"Жанр фильма с id={movie_id} успешно обновлен до {new_genre}")
                return movie
            else:
                print(f"Фильм с id={movie_id} не найден")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении жанра: {e}")
        finally:
            session.close()

    def update_availability(self, movie_id, new_availability):
        session = sessionmaker(bind=self.engine)()
        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if movie:
                movie.is_available = new_availability
                session.commit()
                session.refresh(movie)
                print(
                    f"Доступность фильма с id={movie_id} успешно обновлена до {new_availability}"
                )
                return movie
            else:
                print(f"Фильм с id={movie_id} не найден")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении доступности: {e}")
        finally:
            session.close()

    def delete_by_id(self, movie_id):
        session = sessionmaker(bind=self.engine)()
        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if movie:
                session.delete(movie)
                session.commit()
                print(f"Фильм с id={movie_id} успешно удален")
                return True
            else:
                print(f"Фильм с id={movie_id} не найден")
                return False
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении фильма: {e}")
            return False
        finally:
            session.close()

    def delete_by_title(self, title):
        session = sessionmaker(bind=self.engine)()
        try:
            movie = session.query(Movie).filter(Movie.title == title).first()
            if movie:
                session.delete(movie)
                session.commit()
                print(f"Фильм с названием '{title}' успешно удален")
                return True
            else:
                print(f"Фильм с названием '{title}' не найден")
                return False
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении фильма: {e}")
            return False
        finally:
            session.close()

    def soft_delete(self, movie_id):
        session = sessionmaker(bind=self.engine)()
        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if movie:
                setattr(movie, "is_available", False)
                session.commit()
                session.refresh(movie)
                print(f"Фильм с id={movie_id} сключен из выборки")
                return movie
            else:
                print(f"Фильм с id={movie_id} не найден")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при мягком удалении фильма: {e}")
        finally:
            session.close()


if __name__ == "__main__":
    movie_manager = MovieManager(engine)
    # updated_movie = movie_manager.update_movie(1, title="Побег из Шоушенка",rating=11.0)
    # created_movie = movie_manager.create_movie("Терминатор", "Боевик", 1997, 120, 11.0)
    # all_movies = movie_manager.get_all_movies()
    # for movie in all_movies:
    #     print(movie)
    # by_id = movie_manager.get_by_id(13)
    # print(by_id)
    # updated_movie = movie_manager.update_movie(13,title='Терминатор 2', rating=13.0)
    # print(updated_movie)
    # movie_by_title = movie_manager.get_movie_by_title('Gunshoot')
    # print(movie_by_title)
    # movies_by_genre = movie_manager.get_movies_by_genre('Боевик')
    # for movie in movies_by_genre:
    #     print(movie)
    # movies_by_year = movie_manager.get_movies_by_year(1997)
    # for movie in movies_by_year:
    #     print(movie)
    # movies_by_rating = movie_manager.get_high_rated_movies(8.0)
    # for movie in movies_by_rating:
    #     print(movie)
    # updated_movie = movie_manager.update_rating(13, 9.7)
    # print(updated_movie)
    # update_genre = movie_manager.update_genre(2, 'Триллер')
    # print(update_genre)
    # update_availability = movie_manager.update_availability(11, False)
    # print(update_availability)
    # updated_movie = movie_manager.update_full(13, title='Терминатор 3', rating=9.7, genre='Фантастика')
    # print(updated_movie)
    # deleted_movie = movie_manager.delete_by_id(13)
    # print(deleted_movie)
    # deleted_movie = movie_manager.delete_by_title('Темный рыцарь')
    # print(deleted_movie)
    # sorted_movies = movie_manager.soft_delete(12)
    # print(sorted_movies)
