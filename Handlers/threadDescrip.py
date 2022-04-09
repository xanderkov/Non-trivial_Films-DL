import math
import pickle
import threading
from Database.Database import DataFunFilm, DataFunDist
from Descriptions import Model
from multiprocessing import Pool, Manager
from tqdm import tqdm
import time


def run(id, prepDisc, model, descript_list, q):
    lst = []
    for i in descript_list:
        if i[0] != id:
            d = model.getDistance(i[1], prepDisc)
            if not (math.isinf(d)):
                lst.append([d, i[0]])

    q.put(lst)


def distance(main_desc, id, desc, model):
    d = model.getDistance(main_desc, desc)
    return [d, id]

# def distance(main_desc, id, desc, model, q):
#     d = model.getDistance(main_desc, desc)
#     if not (math.isinf(d)):
#         q.put([d, id])

# def distance(task):
#     d = task[3].getDistance(task[0], task[2])
#     if not (math.isinf(d)):
#         return [d, task[1]]


def split_list(lst, parts=1):
    length = len(lst)
    ret = []
    for i in range(parts):
        ret.append(lst[i * length // parts: (i + 1) * length // parts])

    return ret


def thread_dist(id, descr, films, model, num_thread):
    q = Manager().Queue()
    # task = [[], [], [], []]
    # for i in films:
    #     if i[0] != id:
    #         task[0].append(descr)
    #         task[1].append(i[0])
    #         task[2].append(i[1])
    #         task[3].append(model)

    # task = []
    # for i in films:
    #     if i[0] != id:
    #         task.append([descr, i[0], i[1], model, q])
    task = []
    for i in films:
        if i[0] != id:
            task.append([descr, i[0], i[1], model])

    # print(list(map(distance, task[0], task[1], task[2], task[3])))
    with Pool(processes=num_thread) as pool:
        # pool.starmap(distance, task[0], task[1], task[2], task[3], q)
        lst = pool.starmap(distance, task)
        # pool.close()
        # pool.join()
        # multiple_results = pool.apply_async(distance, task[0], task[1], task[2], task[3])
        # lst = multiple_results.get()
        # multiple_results = [pool.apply_async(distance, task[0], task[1], task[2], task[3]) for i in range(num_thread)]
        # lst = [res.get() for res in multiple_results]
    # lst = q.get()
    lst.sort(key=lambda x: x[0])
    lst = lst[:10]
    return lst


def prep_dist(films, model, db):
    with open('done_ids.txt', 'r') as f:
        done_ids = [int(x) for x in f.read().split()]
        for i in tqdm(films):
            if not (i[0] in done_ids):
                with open('done_ids.txt', 'a') as f:
                    dist = thread_dist(i[0], i[1], films, model, 7)
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
