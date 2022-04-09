from Database.Database import DataFunFilm, DataFunDist
from Descriptions import Model
from multiprocessing import Pool
from tqdm import tqdm
import time


def distance(main_desc, id, desc, model):
    d = model.getDistance(main_desc, desc)
    return [d, id]


def thread_dist(id, descr, films, model, num_thread):
    task = []
    for i in films:
        if i[0] != id:
            task.append([descr, i[0], i[1], model])

    with Pool(processes=num_thread) as pool:
        lst = pool.starmap_async(distance, task, chunksize=len(task)//num_thread)
        lst = lst.get()

    lst.sort(key=lambda x: x[0])
    lst = lst[:10]
    return lst


def prep_dist(films, model, db):
    with open('done_ids.txt', 'r') as f:
        done_ids = [int(x) for x in f.read().split()]
        for i in tqdm(films):
            if not (i[0] in done_ids):
                with open('done_ids.txt', 'a') as f:
                    dist = thread_dist(i[0], i[1], films, model, 16)
                    db.addDistance(i[0], dist)
                    f.write(" " + str(i[0]))
                f.close()


if __name__ == "__main__":
    dbFilm = DataFunFilm()
    films = dbFilm.getTableDF()
    dist = DataFunDist()
    model = Model()
    prepDisc = []
    for i in films["prepare_description"]:
        prepDisc.append(i.split())
    films["prepare_description"] = prepDisc

    prep_dist(list(zip(list(films["kinopoisk_id"]), list(films["prepare_description"]))), model, dist)
