from sqlalchemy import create_engine, DateTime, func, Boolean, Float, PickleType, desc
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query
import time

Base = declarative_base()


class FilmDataBase(Base):
    __tablename__ = 'Kinopoisk_Films'
    id = Column(Integer, primary_key=True)
    kinopoisk_id = Column(Integer)
    imdb_id = Column(Integer)
    name_ru = Column(String)
    name_original = Column(String)
    poster_url = Column(String)
    rating_imdb = Column(Float)
    rating_imdb_vote_count = Column(Integer)
    rating_film_critics = Column(Float)
    rating_critics_vote_count = Column(Integer)
    year = Column(Integer)
    film_length = Column(Integer)
    genres = Column(String)
    web_url = Column(String)
    slogan = Column(String)
    description = Column(String)

    def __init__(self, response):
        self.imdb_id = response.film.imdb_id
        self.kinopoisk_id = response.film.kinopoisk_id
        self.name_ru = response.film.name_ru
        self.name_original = response.film.name_original
        self.poster_url = response.film.poster_url
        self.rating_imdb = response.film.rating_imdb
        self.rating_imdb_vote_count = response.film.rating_imdb_vote_count
        self.rating_film_critics = response.film.rating_film_critics
        self.rating_critics_vote_count = response.film.rating_film_critics_vote_count
        self.year = response.film.year
        self.film_length = response.film.film_length
        self.genres = ' '.join([str(item) for item in response.film.genres])
        self.web_url = response.film.web_url
        self.slogan = response.film.slogan
        self.description = response.film.description


class KinopoiskId(Base):
    __tablename__ = 'Kinopoisk_Id'
    id = Column(Integer, primary_key=True)
    kinopoisk_id = Column(Integer)
    status = Column(String)

    def __init__(self, kinopoisk_id, status):
        self.kinopoisk_id = kinopoisk_id
        self.status = status


class DataFunId(object):

    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine('sqlite:///Database/films.db', echo=False)
        Base.metadata.create_all(self.engine)

    def add_link(self, kinopoisk_id, status):
        session = sessionmaker(bind=self.engine)()

        id = KinopoiskId(kinopoisk_id, status)

        lst = session.query(KinopoiskId).filter(KinopoiskId.kinopoisk_id == kinopoisk_id).first()
        if lst == None:
            session.add(id)
            session.commit()
            return True

        session.close()
        return False

    def getLastId(self):
        session = sessionmaker(bind=self.engine)()
        last = session.query(KinopoiskId).order_by(KinopoiskId.kinopoisk_id.desc()).first()
        if last == None:
            return 1
        session.close()
        return last.kinopoisk_id


class DataFunFilm(object):

    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine('sqlite:///Database/films.db', echo=False)
        Base.metadata.create_all(self.engine)

    def addFilm(self, response):
        session = sessionmaker(bind=self.engine)()

        film = FilmDataBase(response)

        lst = session.query(FilmDataBase).filter(FilmDataBase.kinopoisk_id == film.kinopoisk_id).first()
        if lst == None:
            session.add(film)
            session.commit()
            return True

        session.close()
        return False

    def getLastId(self):
        session = sessionmaker(bind=self.engine)()
        last = session.query(FilmDataBase).order_by(FilmDataBase.kinopoisk_id.desc()).first()
        session.close()
        return last.kinopoisk_id
