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


url = 'https://www.santamariaworld.com/ee/retseptid/'
html = requests.get(url)

soup = BeautifulSoup(html.text, 'html.parser')

lingid = soup.find_all('a', class_ = 'sm-recipe-card__image-link')

for link in lingid:
    print(link.get('href'))