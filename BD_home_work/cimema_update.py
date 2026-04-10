from multiprocessing import managers
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


class MovieViewer:

    @staticmethod
    def print_header(text):
        print("=" * 60)
        print(text)
        print("=" * 60)

    @staticmethod
    def print_statistics(movies):

        if not movies:
            print("Нет данных!")
            return

        total = len(movies)
        total_rating = sum(movie.rating for movie in movies if movie.rating)
        average_rating = total_rating / total if total > 0 else 0
        available = sum(1 for movie in movies if movie.is_available)
        not_available = total - available
        years = [movie.year for movie in movies if movie.year]
        min_year = min(years) if years else "-"
        max_year = max(years) if years else "-"

        print("=" * 60)
        print("СТАТИСТИКА ПО ФИЛЬМАМ")
        print("=" * 60)
        print("Всего фильмов:", total)
        print("Средний рейтинг:", round(average_rating, 2))
        print("Доступных:", available)
        print("Недоступных:", not_available)
        print("Год выпуска: от", min_year, "до", max_year)
        print("=" * 60)

    def print_all(self, movies):

        if not movies:
            print("Фильмов не найдено.")

            return

        print("=" * 80)
        print("ID | Название | Жанр | Год | Рейтинг | Доступен")
        print("-" * 80)

        for movie in movies:
            availability = "Доступен" if movie.is_available else "Недоступен"
            print(
                movie.id,
                movie.title,
                movie.genre,
                movie.year,
                movie.rating,
                availability,
                sep=" | ",
            )

        print("=" * 80)
        print("Количество фильмов в базе данных:", len(movies))

    def print_one(self, movie):
        """Выводит один фильм в красивом формате"""

        if not movie:
            print("Фильм не найден!")
            return

        print("=" * 60)
        print("ID:", movie.id)
        print("Название:", movie.title)
        print("Жанр:", movie.genre)
        print("Год:", movie.year)
        print("Рейтинг:", movie.rating)
        print("Длительность:", movie.duration, "мин")
        availability = "Да" if movie.is_available else "Нет"
        print("Доступен:", availability)
        print("=" * 60)


if __name__ == "__main__":
    # manager = MovieManager(engine)
    # all_movies = manager.get_all_movies()
    # MovieViewer.print_header("Список всех фильмов")
    # print(
    #     """Номера id могут идти не по порядку - потому-что некоторые фильмы были удалены, а другие добавлены  в  базу данных."""
    # )
    # MovieViewer().print_all(all_movies)
    # print()
    # MovieViewer.print_header("Вывод одного фильма")
    # movie = manager.get_movie_by_title("Терминатор")
    # MovieViewer().print_one(movie)
    # print()
    # print()
    # MovieViewer().print_statistics(all_movies)
    pass
