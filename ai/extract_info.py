import requests
from bs4 import BeautifulSoup
import datetime
import asyncio
import aiohttp

 #funktsioon millega eraldada retsepti leheküljelt koostisained
async def getinfo_from_links(links):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_parse(session, link) for link in links]
        results = await asyncio.gather(*tasks)
        return results

async def fetch_and_parse(session, link):
    async with session.get(link, ssl=False) as response:
        r_text = await response.text()
        soup = BeautifulSoup(r_text, 'html.parser')
        ul_tag = soup.find('ul', class_='td-arrow-list')
        if ul_tag:
            ingredients = []
            for li in ul_tag.find_all('li'):
                ingredients.append(li.get_text())
            return (ingredients, link)
        else:
            return False

def getinfo_Retseptisahtel(x):
    #base url kus x = leheküljenumber
    url = f'https://retseptisahtel.ee/retseptid/page/{x}/'
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #eraldan leheküljelt retseptide lingid
    h3_tags = soup.find_all('h3', class_='entry-title td-module-title')
    a_tags = [a_tag.find('a') for a_tag in h3_tags]
    links = []
    for link in a_tags:
        links.append(link.get('href'))
    #annan kõik leitud lingid funktsiooni getinfo_from_links, mis leiab info kõikidelt lehtedelt samaaegselt
    results = asyncio.run(getinfo_from_links(links))
    page_info = []
    for info in results:
        if info:
            page_info.append(info)
    if page_info:
        return page_info
    else:
        return

# no session 0:00:07.329809
# with session 0:00:05.461197
# total time ?
if __name__ == '__main__':
    s = requests.Session()
    start = datetime.datetime.now()
    with open('ingredients.txt', 'w', encoding='UTF-8') as file:
        for i in range(1, 90):
            page_info = getinfo_Retseptisahtel(i)
            if page_info:
                file.write(f'Page {i}\n')
                for n, (ingredients, link) in enumerate(page_info, 1):
                    ingredients_str = ", ".join(ingredients)
                    file.write(f'{n} - {ingredients} | {link}\n')
                file.write('\n\n')
                print(i)

    finish = datetime.datetime.now() - start
    print(finish)