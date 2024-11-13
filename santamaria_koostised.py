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
    
    for link in lingid:
        print(link.get('href'))


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


## SIIT ALGAVAD PÕHIPROGRAMMI FUNKT.
# funktsioon võtab failist iga eraldi retsepti ja väljastab iga retsepti omakorda listina
def andmed_failist(fail):
    lst_retsept = []
    with open(fail, encoding='UTF-8') as f:
        for rida in f:
            retsept = []
            üks_retsept = rida.strip().split(' | ')
            lst_päris = ast.literal_eval(üks_retsept[0])
            retsept.append(lst_päris)
            retsept.append(üks_retsept[1])
            lst_retsept.append(retsept)

    return lst_retsept


#järjend 1 peab olema retsepti järjend ja jär2 on külmiku jääkide järjend
#funktsioon leiab ühiste sõnade arvu mõlemas järjendis
def andmete_ühilduvus(jär1, jär2):
    ühised_sõnad = []
    for el in jär1:
        sõne_lst = el.split()
        for sõne in sõne_lst:
            for sõne2 in jär2:
                if sõne2 in sõne:
                    ühised_sõnad.append(sõne_lst)
                
                # if len(sõne2) > 3:
                #     if sõne2[:4] == sõne[:4]:
                #         ühised_sõnad.append(sõne_lst)
                # else:
                #     if sõne2[:3] == sõne[:3]:
                #         ühised_sõnad.append(sõne_lst)
    return len(ühised_sõnad)


def main():
    külmik = input('Sisesta külmiku jäägid nt(vahukoor pasta): ')
    lst_külmik = külmik.split()
    lst_retsept = andmed_failist('santamaria_koostisosad.txt')
    suurim_sarnasus = 0
    count = 0
    
    ## leiab suurima sarnanuse üle kõikide retseptide
    for retsept in lst_retsept:
        ühised = andmete_ühilduvus(retsept[0], lst_külmik)
        if ühised > suurim_sarnasus:
            suurim_sarnasus = ühised
    
    #väljastab suurimate sarnastustega retseptide lingid
    for retsept in lst_retsept:
        if suurim_sarnasus == andmete_ühilduvus(retsept[0], lst_külmik):
            print (retsept[1])
            count += 1
            if count == 5:
                break

    print(suurim_sarnasus)

if __name__ == '__main__':
    main()





