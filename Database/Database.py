from ast import Str
from numpy import short
from sqlalchemy import create_engine, DateTime, func, Boolean, Float, PickleType, desc
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query
import pandas as pd
import re
import yadisk
from zipfile import ZipFile
from Database.constants import YANDEX_TOKEN
from sqlalchemy import or_, and_

Base = declarative_base()


def dispatch():
    zipObj = ZipFile('db.zip', 'w')
    zipObj.write('films.db')
    zipObj.close()
    print("ziped")
    y = yadisk.YaDisk(token=YANDEX_TOKEN)
    y.upload("db.zip", "/Non-trivial_Films-DL/db.zip")
    print("uploaded") 


def download():
    y = yadisk.YaDisk(token=YANDEX_TOKEN)
    y.download("/Non-trivial_Films-DL/db.zip", "db.zip")
    print("downloaded")
    z = ZipFile('db.zip', 'r')
    z.extractall()
    print("unzipped")


def fixGenres(genre):
    orig_gen = re.findall(r'\'(\w+)\'', genre)
    if orig_gen != []:
        fix_gen = " ".join(orig_gen)
        genre = fix_gen
    return genre


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
    rating_kinopoisk = Column(Integer)
    short_desription = Column(String)
    rating_age_limits = Column(Integer)
    prepare_description = Column(String)

    def __init__(self, response, prep):
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
        self.genres = fixGenres(' '.join([str(item) for item in response.film.genres]))
        self.web_url = response.film.web_url
        self.slogan = response.film.slogan
        self.description = response.film.description
        self.rating_kinopoisk = response.film.rating_kinopoisk
        self.short_desription = response.film.short_description
        self.rating_age_limits = response.film.rating_age_limits
        self.prepare_description = prep.tag_ud(response.film.description)
        
        
class FilmDistTable(Base):
    __tablename__ = 'Film_Dist_Table'
    id = Column(Integer, primary_key=True)
    id_first = Column(Integer)
    id_second = Column(Integer)
    distance = Column(Float)

    def __init__(self, id_first, id_second, distance):
        self.id_first = id_first
        self.id_second = id_second
        self.distance = distance


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
        self.engine = create_engine('sqlite:///../Database/films.db', echo=False)
        Base.metadata.create_all(self.engine)

    def add_link(self, kinopoisk_id, status):
        session = sessionmaker(bind=self.engine)()

        id = KinopoiskId(kinopoisk_id, status)

        lst = session.query(KinopoiskId).filter(KinopoiskId.kinopoisk_id == kinopoisk_id).first()
        if lst is None:
            session.add(id)
            session.commit()
            return True

        session.close()
        return False

    def id_update(self, kinopoisk_id, status="done"):
        session = sessionmaker(bind=self.engine)()
        lst = session.query(KinopoiskId).filter(KinopoiskId.kinopoisk_id == kinopoisk_id).first()
        lst.status = status
        session.commit()
        session.close()

    def get_id_to_pars(self):
        session = sessionmaker(bind=self.engine)()

        lst = session.query(KinopoiskId).filter(KinopoiskId.status == "ready")
        lst_id = []
        for i in lst:
            lst_id.append(i.kinopoisk_id)
        session.close()
        return lst_id

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
        self.engine = create_engine('sqlite:///../Database/films.db')
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

    def getFilmById(self, id):
        session = sessionmaker(bind=self.engine)()
        film = session.query(FilmDataBase).filter(FilmDataBase.kinopoisk_id == id).first()
        session.close()
        return film

    def getLastId(self):
        session = sessionmaker(bind=self.engine)()
        last = session.query(FilmDataBase).order_by(FilmDataBase.kinopoisk_id.desc()).first()
        session.close()
        return last.kinopoisk_id

    def getTableDF(self):
        df = pd.read_sql('SELECT * FROM Kinopoisk_Films', self.engine)
        return df

    def fexGenres(self):
        session = sessionmaker(bind=self.engine)()
        lst = session.query(FilmDataBase)
        for film in lst:
            orig_gen = re.findall(r'\'(\w+)\'', film.genres)
            if orig_gen != []:
                fix_gen = " ".join(orig_gen)
                film.genres = fix_gen
        session.commit()
        session.close()

    def remakeDescriprionToArray(self):
        session = sessionmaker(bind=self.engine)()
        lst = session.query(FilmDataBase)
        description_array = []
        for film in lst:
            separeted = re.split(" ", film.description)
            words = []
            for word in separeted:
                words.append(word.lower())
            description_array.append(words)
        session.commit()
        session.close()
        return description_array

    def addPrepDescription(self, id, descrp):
        session = sessionmaker(bind=self.engine)()
        film = session.query(FilmDataBase).filter(FilmDataBase.kinopoisk_id == id).first()
        if film is None:
            return False
        film.prepare_description = descrp
        session.commit()
        session.close()
        return True


class DataFunDist(object):

    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine('sqlite:///../Database/films.db')
        Base.metadata.create_all(self.engine)

    def addDistance(self, first, distance):
        session = sessionmaker(bind=self.engine)()

        for i in distance:
            dist = FilmDistTable(first, i[1], i[0])
            session.add(dist)

        session.commit()
        session.close()


if __name__ == '__main__':
    dispatch()