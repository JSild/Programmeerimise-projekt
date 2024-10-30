import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin #lisab base urlile juurde valuesid

## TO-DO
## 1. extracti lingid kõigilt 


#1. add url agent (OPTIONAL)
#headers = {}

#2. Base URL
url = 'https://retseptisahtel.ee/retseptid/'

#3. cycle through pages
while True:
    #5. Send get() req and fetch contents
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    footer = soup.select_one('span.pages')
    print(footer.text.strip())