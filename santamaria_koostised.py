import time
import requests
import ast
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

## funktsioon leiab santamaria lehelt kõikide erinevate retseptide lingid
def lingid_santamaria():
    driver = webdriver.Chrome()
    url = 'https://www.santamariaworld.com/ee/retseptid/'
    driver.get(url)
    # Automaat scroll
    scroll_pause_time = 2  # paus scrolli tagant
    screen_height = driver.execute_script("return window.screen.height;")  # Window kõrgus
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        # Kontroll kas veebilehe lõpus
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    lingid = soup.find_all('a', class_ = 'sm-recipe-card__image-link')
    with open('santamaria_lingid.txt', 'w', encoding='UTF-8') as fail:
        for link in lingid:
            fail.writelines(f"{link.get('href')}\n")


## funktsioon leiab igast lingist koostis osad ja kirjutab faili need koostisosad listina + lingi.

def koostisosad():
    file = open('santamaria_lingid.txt', encoding='UTF-8')
    file2 = open('santamaria_koostisosad.txt', 'w', encoding='UTF-8')
    koostisosad_list = []

    while True:
        lingi_algus = 'https://www.santamariaworld.com'
        lingi_lõpp = file.readline().strip()
        url = lingi_algus + lingi_lõpp
        if url == 'https://www.santamariaworld.com':
            break
        html = requests.get(url)

        soup = BeautifulSoup(html.content, 'html.parser')

        tabel = soup.find_all('td')
        koostisosad_list = []

        for x in tabel:
            koostisosad_ = x.text.strip().split()
            ing = (' ').join(koostisosad_)
            koostisosad_list.append(ing)

        file2.write(str(koostisosad_list) + ' | ' + url + '\n')
        
    file.close()
    file2.close()

lingid_santamaria()
koostisosad()







