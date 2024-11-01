from bs4 import BeautifulSoup
import requests


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


        

koostisosad()


