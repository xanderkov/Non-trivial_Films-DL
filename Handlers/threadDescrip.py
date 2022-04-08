import math
import pickle
import threading
from Database.Database import DataFunFilm, DataFunDist
from Descriptions import Model
from queue import Queue
from tqdm import tqdm
import time


class DThread(threading.Thread):
    def __init__(self, id, prepDisc, model, descript_list, q):
        threading.Thread.__init__(self)
        self.id = id
        self.prepDisc = prepDisc
        self.model = model
        self.descript_list = descript_list
        self.q = q

    def run(self):
        lst = []
        for i in self.descript_list:
            if i[0] != self.id:
                d = self.model.getDistance(i[1], self.prepDisc)
                if not (math.isinf(d)):
                    lst.append([d, i[0]])

        self.q.put(lst)


def split_list(lst, parts=1):
    length = len(lst)
    ret = []
    for i in range(parts):
        ret.append(lst[i * length // parts: (i + 1) * length // parts])

    return ret


def thread_dist(id, descr, films, model, num_thread):
    films_split = split_list(films, num_thread)
    q = Queue()
    threads = []
    for i in range(num_thread):
        threads.append(DThread(id, descr, model, films_split[i], q))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    lst = []
    for i in q.queue:
        lst.extend(i)
    lst.sort(key=lambda x: x[0])
    lst = lst[:100]
    return lst


def prep_dist(films, model, db):
    with open('done_ids.txt', 'r') as f:
        done_ids = [int(x) for x in f.read().split()]
    with open('done_ids.txt', 'a') as f:
        for i in tqdm(films):
            if not (i[0] in done_ids):
                timing = time.time()
                dist = thread_dist(i[0], i[1], films, model, 2)
                print("\n")
                print(time.time() - timing)
                break
                # db.addDistance(i[0], dist)
                f.write(" "+i[0])
                pickle.dump(done_ids, f)
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
