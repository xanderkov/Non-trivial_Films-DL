from bs4 import BeautifulSoup
import requests as req
from Database import DataFunId
import time

if __name__ == '__main__':
    idDB = DataFunId()
    for i in range(idDB.getLastId(),1000000):
        resp = req.get("https://www.kinopoisk.ru/film/{}/".format(i))
        soup = BeautifulSoup(resp.text, 'lxml')
        p = soup.prettify()
        f = soup.find_all("div", class_="CheckboxCaptcha-Label")
        if len(f) == 0:
            f = soup.find_all("div", class_="error-page")
            if len(f) == 0:
                idDB.add_link(i, "redy")
                print("{} redy".format(i))
            else:
                idDB.add_link(i, "empty")
                print("{} empty".format(i))
        else:
            print("Error: robot checking while {}".format(i))
            break
        time.sleep(10)