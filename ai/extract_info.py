import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin #lisab base urlile juurde valuesid
import datetime


def getinfo_Retseptisahtel(x):
    #funktsioon millega eraldada retsepti leheküljelt koostisained
    def getinfo_from_link(link):
        start = datetime.datetime.now()
        r = s.get(link)
        finish = datetime.datetime.now() - start
        print(f'Lingi fetchimine {finish}')
        start = datetime.datetime.now()
        soup = BeautifulSoup(r.text, 'html.parser')
        ul_tag = soup.find('ul', class_='td-arrow-list')
        if ul_tag:
            ingredients = []
            for li in ul_tag.find_all('li'):
                ingredients.append(li.get_text())
            finish = datetime.datetime.now() - start
            print(f'Lingi parsimine {finish}')
            return ingredients
        else:
            return False

    #base url kus x = leheküljenumber
    url = f'https://retseptisahtel.ee/retseptid/page/{x}/'
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #eraldan leheküljelt retseptide lingid
    h3_tags = soup.find_all('h3', class_='entry-title td-module-title')
    a_tags = [a_tag.find('a') for a_tag in h3_tags]
    for link in a_tags:
        link = link.get('href')
        info = getinfo_from_link(link)
        if info:
            print(info)

    return

# no session 0:00:07.329809
# with session 0:00:05.461197
if __name__ == '__main__':
    s = requests.Session()
    start = datetime.datetime.now()
    for i in range(24, 27):
        getinfo_Retseptisahtel(i)
        print(i)
    finish = datetime.datetime.now() - start
    print(finish)