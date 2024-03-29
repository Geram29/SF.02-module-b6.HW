# Импортируем необходимые библиотеки
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def is_int(str):
    """
    Проверяет строку на число (для валидации года выпуска альбома)
    """
    try:
        int(str)
        return True
    except ValueError:
        return False


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def add(album_data):
    """
    Проверяет запрос по новому альбому
    """
    session = connect_db()

    new_Album = session.query(Album).filter(Album.album == album_data["album"].title()).first()

    if  new_Album == None:
        #если такого альбома в БД нет, то сохраняем его в БД
        session.add(Album(year=album_data["year"], artist=album_data["artist"].title(), genre=album_data["genre"].title(), album=album_data["album"].title()))
        session.commit()
        return True
    else:
        return False
