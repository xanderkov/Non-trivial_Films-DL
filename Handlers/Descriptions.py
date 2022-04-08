import math
import gensim
import wget
import zipfile
from Database.Database import DataFunDist, DataFunFilm
from tqdm import tqdm
import pickle


class Model(object):
    model_url = 'http://vectors.nlpl.eu/repository/20/220.zip'

    def __init__(self):
        model_file = self.model_url.split('/')[-1]
        with zipfile.ZipFile(model_file, 'r') as archive:
            stream = archive.open('model.bin')
            self.model = gensim.models.KeyedVectors.load_word2vec_format(stream, binary=True)

    def download(self):
        wget.download(self.model_url)

    def getDistance(self, first, second):
        return self.model.wmdistance(first, second,  norm=True)


def moreSimilar(films, id, prepDisc, model):
    lst = []
    for i in films:
        if i[0] != id:
            d = model.getDistance(i[1], prepDisc)
            if not(math.isinf(d)):
                lst.append([d, i[0]])
    lst.sort(key=lambda x: x[0])
    lst = lst[:100]
    return lst


def prep_dist(films, model, db):
    with open('done_ids.pkl', 'rb') as f:
        done_ids = pickle.load(f)
        f.close()
    with open('done_ids.pkl', 'wb') as f:
        for i in tqdm(films):
            if not (i[0] in done_ids):
                dist = moreSimilar(films, i[0], i[1], model)
                db.addDistance(i[0], dist)
                done_ids.append(i[0])
                pickle.dump(done_ids, f)
    f.close()


def main():
    dbFilm = DataFunFilm()
    films = dbFilm.getTableDF()
    dist = DataFunDist()
    model = Model()
    prepDisc = []
    for i in films["prepare_description"]:
        prepDisc.append(i.split())
    films["prepare_description"] = prepDisc

    prep_dist(list(zip(list(films["kinopoisk_id"]), list(films["prepare_description"]))), model, dist)


if __name__ == "__main__":
    main()
