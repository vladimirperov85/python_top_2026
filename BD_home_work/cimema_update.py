from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
)

engine = create_engine(
    "sqlite:///C:/Users/PC/Desktop/WINDOWS(HOME REPOZITORY)/BD_home_work/My_bd.db",
    echo=False,
)

Base = declarative_base()


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    movies = relationship("Movie", back_populates="genre")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    year = Column(Integer)
    rating = Column(Float)
    duration = Column(Integer)
    is_available = Column(Boolean, default=True)
    genre = relationship("Genre", back_populates="movies")

    def __repr__(self):
        genre_name = self.genre.name if self.genre else "Без жанра"
        return f"<Movie(id={self.id}, title='{self.title}', genre='{genre_name}', year={self.year}, rating={self.rating}, available={self.is_available})>"


class MovieManager:

    def __init__(self, engine):
        self.engine = engine

    def create_movie(self, title, genre, year, duration, rating):
        session = sessionmaker(bind=self.engine)()
        try:
            # Поиск жанра по названию
            genre_obj = session.query(Genre).filter(Genre.name == genre).first()
            if not genre_obj:
                print(f"Жанр '{genre}' не найден. Создание нового жанра...")
                genre_obj = Genre(name=genre)
                session.add(genre_obj)
                session.commit()
                session.refresh(genre_obj)

            new_movie = Movie(
                title=title,
                genre_id=genre_obj.id,
                year=year,
                duration=duration,
                rating=rating,
            )
            session.add(new_movie)
            session.commit()
            session.refresh(new_movie)
            print(f"Фильм {title} добавлен в базу данных id ={new_movie.id}")
            return new_movie
        except Exception as e:
            session.rollback()
            print(f"Ошибка при создании фильма: {e}")
            return None
        finally:
            session.close()

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
        try:
            genre_obj = session.query(Genre).filter(Genre.name == genre).first()
            if not genre_obj:
                print(f"Жанр '{genre}' не найден")
                return []
            movies = session.query(Movie).filter(Movie.genre_id == genre_obj.id).all()
            return movies
        except Exception as e:
            print(f"Ошибка при поиске фильмов по жанру: {e}")
            return []
        finally:
            session.close()

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
                genre_obj = session.query(Genre).filter(Genre.name == new_genre).first()
                if not genre_obj:
                    print(f"Жанр '{new_genre}' не найден. Создание нового жанра...")
                    genre_obj = Genre(name=new_genre)
                    session.add(genre_obj)
                    session.commit()
                    session.refresh(genre_obj)
                movie.genre_id = genre_obj.id
                session.commit()
                session.refresh(movie)
                print(f"Жанр фильма с id={movie_id} успешно обновлен до '{new_genre}'")
                return movie
            else:
                print(f"Фильм с id={movie_id} не найден")
                return None
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении жанра: {e}")
            return None
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


class GenreManager:

    def __init__(self, engine):
        self.engine = engine
        Base.metadata.create_all(engine)

    def create(self, name, description):
        new_genre = Genre(name=name, description=description)
        session = sessionmaker(bind=self.engine)()
        session.add(new_genre)
        session.commit()
        session.refresh(new_genre)
        session.close()
        print(f"Жанр '{name}' добавлен в базу данных ID = {new_genre.id}")
        return new_genre

    def get_all(self):
        session = sessionmaker(bind=self.engine)()
        genres = session.query(Genre).all()
        session.close()
        return genres

    def get_by_id(self, genre_id):
        session = sessionmaker(bind=self.engine)()
        genre = session.query(Genre).filter(Genre.id == genre_id).first()
        session.close()
        return genre

    def get_genres_with_movies_count(self):
        from sqlalchemy import func

        session = sessionmaker(bind=self.engine)()

        results = (
            session.query(
                Genre,
                func.count(Movie.id).label("movie_count"),
            )
            .outerjoin(Movie, Genre.id == Movie.genre_id)
            .group_by(Genre.id)
            .all()
        )

        session.close()

        genre_counts = []
        for genre_obj, count in results:
            genre_counts.append(
                {
                    "genre_object": genre_obj,
                    "movie_count": count,
                }
            )

        return genre_counts

    def get_by_name(self, name):
        session = sessionmaker(bind=self.engine)()
        genre = session.query(Genre).filter(Genre.name == name).first()
        session.close()
        return genre

    def update_name(self, genre_id, new_name):
        session = sessionmaker(bind=self.engine)()
        try:
            genre = session.query(Genre).filter(Genre.id == genre_id).first()
            if genre:
                genre.name = new_name
                session.commit()
                session.refresh(genre)
                print(
                    f"Название жанра с id={genre_id} успешно обновлено до '{new_name}'"
                )
                return genre
            else:
                print(f"Жанр с id={genre_id} не найден")
                return None
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении названия жанра: {e}")
            return None
        finally:
            session.close()

    def update_description(self, genre_id, new_desc):
        session = sessionmaker(bind=self.engine)()
        try:
            genre = session.query(Genre).filter(Genre.id == genre_id).first()
            if genre:
                genre.description = new_desc
                session.commit()
                session.refresh(genre)
                print(f"Описание жанра с id={genre_id} успешно обновлено")
                return genre
            else:
                print(f"Жанр с id={genre_id} не найден")
                return None
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении описания жанра: {e}")
            return None
        finally:
            session.close()

    def delete_by_id(self, genre_id):
        session = sessionmaker(bind=self.engine)()
        try:
            genre = session.query(Genre).filter(Genre.id == genre_id).first()
            if genre:
                session.delete(genre)
                session.commit()
                print(f"Жанр с id={genre_id} ('{genre.name}') успешно удален.")
                return True
            else:
                print(f"Жанр с id={genre_id} не найден.")
                return False
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении жанра: {e}")
            return False
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
            genre_name = movie.genre.name if movie.genre else "Без жанра"
            print(
                movie.id,
                movie.title,
                genre_name,
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
        print("Жанр:", movie.genre.name if movie.genre else "Без жанра")
        print("Год:", movie.year)
        print("Рейтинг:", movie.rating)
        print("Длительность:", movie.duration, "мин")
        availability = "Да" if movie.is_available else "Нет"
        print("Доступен:", availability)
        print("=" * 60)


class CinemaViewer:
    """Класс для отображения связей между жанрами и фильмами."""

    def print_all_genres_with_movies(self, genres, movies):
        
        print("\n" + "=" * 60)
        print("КАТАЛОГ КИНОТЕАТРА: ЖАНРЫ И ФИЛЬМЫ")
        print("=" * 60)

        if not genres:
            print("Жанры не найдены!")
            return

        # Считаем фильмы по каждому жанру
        print(f"\nВсего жанров: {len(genres)}")
        print(f"Всего фильмов: {len(movies)}\n")

        print("Распределение фильмов по жанрам:")
        print("-" * 60)

        for genre in genres:
            # Считаем фильмы этого жанра через связь по genre_id
            genre_movies_count = sum(1 for m in movies if m.genre_id == genre.id)
            print(f"  {genre.name:<25} — {genre_movies_count} фил.")

        # Считаем фильмы без жанра
        no_genre_count = sum(1 for m in movies if not m.genre_id)
        if no_genre_count > 0:
            print(f"  {'Без жанра':<25} — {no_genre_count} фил.")

        print("-" * 60)
        print(f"ВСЕГО: {len(genres)} жанров, {len(movies)} фильмов")
        print("=" * 60)


if __name__ == "__main__":
    "Необходимо подключиться к своей базе данных что бы увидеть все жанры и фильмы в этих жанрах а так же связи между таблицами"
    Base.metadata.create_all(engine)

    genre_manager = GenreManager(engine)
    movie_manager = MovieManager(engine)
    cinema_viewer = CinemaViewer()

    # Получаем данные
    genres = genre_manager.get_all()
    movies = movie_manager.get_all_movies()

    # Выводим каталог с связями жанров и фильмов
    cinema_viewer.print_all_genres_with_movies(genres, movies)
