from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from constants import TOKEN
from Database import DataFunFilm
import time


def parser():
    api_client = KinopoiskApiClient(TOKEN)
    filmDB = DataFunFilm()
    last_id = filmDB.getLastId()
    n = last_id + 1
    for i in range(last_id, n):
        try:
            time.sleep(0.1)
            request = FilmRequest(i)
            response = api_client.films.send_film_request(request)
            response.film.genres
            if filmDB.addFilm(response):
                print('Added {}'.format(response.film.kinopoisk_id))
            else:
                print('Id is already in the database {}'.format(response.film.kinopoisk_id))

        except Exception as error:
            print('Id is not capable ' + str(error))
            
if __name__ == '__main__':
    parser()