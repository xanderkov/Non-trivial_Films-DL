from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from Parse.constants import TOKEN
from Database.Database import DataFunFilm, DataFunId
import time


def parser():
    api_client = KinopoiskApiClient(TOKEN)
    filmDB = DataFunFilm()
    last_id = filmDB.getLastId()
    n = last_id + 100
    for i in range(302, 305):
        try:
            request = FilmRequest(i)
            response = api_client.films.send_film_request(request)
            if filmDB.addFilm(response):
                print('Added {}'.format(response.film.kinopoisk_id))
            else:
                print('Id is already in the database {}'.format(response.film.kinopoisk_id))
        except Exception as error:
            print('Id is not capable ' + str(error))


def parserInListId():
    api_client = KinopoiskApiClient(TOKEN)
    filmDB = DataFunFilm()
    idDB = DataFunId()
    id_lst = idDB.get_id_to_pars()
    for i in id_lst:
        try:
            request = FilmRequest(i)
            response = api_client.films.send_film_request(request)
            if filmDB.addFilm(response):
                print('Added {}'.format(i))
            else:
                print('Id is already in the database {}'.format(i))
            idDB.id_update(i)

        except Exception as error:
            print('Id is not capable ' + str(error))
        if i % 20 == 0:
            time.sleep(1)


if __name__ == '__main__':
    parserInListId()