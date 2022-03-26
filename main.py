from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from constants import TOKEN
import numpy as np
from sqlalchemy import create_engine, DateTime, func, Boolean, Float, PickleType
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query

Base = declarative_base()



class FilmDataBase(Base):
    __tablename__='Kinopoisk_Films'
    id = Column(Integer, primary_key=True)
    imdb_id = Column(Integer)
    name_ru = Column(String)
    name_en = Column(String)
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
        self.name_ru = response.film.name_ru
        self.name_en = response.film.name_en
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


class DataBaseAddition(object):
    
    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine('sqlite:///films.db', echo=False)
        Base.metadata.create_all(self.engine)
        
    
    def addFilm(self, response):
        session = sessionmaker(bind=self.engine)()
        film = FilmDataBase(response)
        
        session.add(film)
        session.commit()
        session.close()

    
    

def main():
    
    api_client = KinopoiskApiClient(TOKEN)
    filmDB = DataBaseAddition()
    for i in range(1000, 2000):
        try:
            request = FilmRequest(i)
            response = api_client.films.send_film_request(request)
            response.film.genres
            filmDB.addFilm(response)
            print('Checked {}'.format(i))
        except Exception as error:
            print('Id is not capable ' + str(error))
        
          

if __name__=='__main__':
    main()
