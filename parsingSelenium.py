import time
from selenium import webdriver
from bs4 import BeautifulSoup
from Database import DataFunId

options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
chrome_driver_binary = "D:\chromedriver_win32\chromedriver.exe"
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(r"C:\Users\yaros\chromedriver_win32\chromedriver.exe")


if __name__ == '__main__':
    idDB = DataFunId()
    driver.set_window_size(1920, 1080)
    driver.get("https://www.kinopoisk.ru/top/navigator/m_act[num_vote]/100/m_act[rating]/1%3A/order/rating/page/1/#results")
    print("Enter the capcha , after input smf")
    input()
    soup = BeautifulSoup(driver.page_source, 'lxml')

    for i in range(10, 305):
        films = soup.find_all("div", class_="item _NO_HIGHLIGHT_")
        for film in films:
            raw_id = film['id']
            raw_id = raw_id[3:]
            if idDB.add_link(raw_id, "redy") :
                print("{} redy".format(raw_id))
            else:
                print("{} in DB".format(raw_id))
        # content = driver.find_element(by=By.XPATH, value="//*[@class='item _NO_HIGHLIGHT_']")
        driver.get(
            "https://www.kinopoisk.ru/top/navigator/m_act[num_vote]/100/m_act[rating]/1%3A/order/rating/page/{}/#results".format(i))
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        pass



