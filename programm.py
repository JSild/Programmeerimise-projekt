################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt Vare
# Teema:
#
#
# Autorid:
#
# mõningane eeskuju:
#
# Lisakommentaar (nt käivitusjuhend):
#
##################################################

import requests
from bs4 import BeautifulSoup 
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time

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

    for link in lingid:
        print(link.get('href'))

lingid_santamaria()