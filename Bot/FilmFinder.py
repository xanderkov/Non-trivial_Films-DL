from Database.Database import DataFunFilm, DataFunDist
from Handlers.Descriptions import Model
from tqdm import tqdm
import math


def distance(main_desc, id, desc, model):
    d = model.getDistance(main_desc, desc)
    return [d, id]


def get_distance(id, descr, films, model):
    lst = []
    descr = descr.split()
    for i in tqdm(films):
        if i[0] != id:
            d = model.getDistance(i[1], descr)
            lst.append([d, i[0]])
    lst.sort(key=lambda x: x[0])
    lst = lst[:10]
    return lst


def prep_dist(films, model, film):
    distance = get_distance(film.kinopoisk_id, film.prepare_description, films, model)
    dbFilm = DataFunFilm()
    nearest_films = []
    for i in distance:
        film_i = dbFilm.getFilmById(i[1])
        nearest_films.append([film_i.name_ru, film_i.web_url])
    return nearest_films


def find_film(filmName):
    dbFilm = DataFunFilm()
    films = dbFilm.getTableDF()
    model = Model()
    film = dbFilm.getFilmByName(filmName)
    if film == None:
        film = dbFilm.getFilmByUrl(filmName)
    if film != None:
        prepDisc = []
        for i in films["prepare_description"]:
            prepDisc.append(i.split())
        films["prepare_description"] = prepDisc
        return prep_dist(list(zip(list(films["kinopoisk_id"]), list(films["prepare_description"]))), model, film)
    return None


if __name__ == "__main__":
    find_film("Матрица")
