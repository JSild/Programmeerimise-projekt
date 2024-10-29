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
from bs4 import BeautifulSoup
import requests
import re



def urlTOhtml(url):
    html = requests.get(url)
    return html.text

def mariliisilover_retsepti_elemendid_listina(link):
    retsepti_html = urlTOhtml(link)
    supp = BeautifulSoup(retsepti_html, 'html.parser')
    elemendid0 = supp.find_all(class_=['cookbook-ingredient', 'cookbook-ingredient-item'])
    elemendid1 = supp.find('div', dir_='ltr')
    elemendid_lst = []
    if elemendid1:
        for element in elemendid1.find('p').strings:
            elemendid_lst.append(element.strip())
    else:
        for element in elemendid0:
            elemendid_lst.append(element.text)
    return elemendid_lst, link
    

mariliisilover = 'https://mariliisilover.com/retseptide-indeks/'
mariliisilover_html = urlTOhtml(mariliisilover)
supp = BeautifulSoup(mariliisilover_html, 'html.parser')


main_tag = supp.find('main')
for link in main_tag.find_all('a', attrs={'href': re.compile("^https://mariliisilover.com")}):
    print(mariliisilover_retsepti_elemendid_listina(link.get('href')))

