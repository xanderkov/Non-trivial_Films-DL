from Database.Database import DataFunFilm, DataFunDist
from Handlers.Descriptions import Model
from tqdm import tqdm


def distance(main_desc, id, desc, model):
    d = model.getDistance(main_desc, desc)
    return [d, id]


def get_distrance(id, descr, films, model):
    task = []
    lst = []
    for i in films:
        if i[0] != id:
            lst.append(distance(descr, i[0], i[1], model))

    lst.sort(key=lambda x: x[0])
    lst = lst[:10]
    return lst


def prep_dist(films, model, film):

    distance = get_distrance(film.kinopoisk_id, film.description, films, model)
    dbFilm = DataFunFilm()
    films_base = dbFilm.getTableDF()
    near_films = []
    for i in distance:
        film_i = dbFilm.getFilmById(i[1])
        near_films.append(film_i.name_ru)
    return near_films


def find_film(filmName):
    dbFilm = DataFunFilm()
    films = dbFilm.getTableDF()
    model = Model()
    film = dbFilm.getFilmByName(filmName)
    prepDisc = []
    for i in films["prepare_description"]:
        prepDisc.append(i.split())
    films["prepare_description"] = prepDisc
    return prep_dist(list(zip(list(films["kinopoisk_id"]), list(films["prepare_description"]))), model, film)
