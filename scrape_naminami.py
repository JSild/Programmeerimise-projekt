import requests
from bs4 import BeautifulSoup
import re

def koostisosad():
    # Open the file containing links
    with open('korras_nami-nami_lingid.txt', encoding='UTF-8') as file:
        # Open a file to write the ingredients
        with open('nami-nami_koostisosad.txt', 'w', encoding='UTF-8') as file2:
            for url in file:
                url = url.strip()
                if not url:
                    continue
                
                try:
                    # Get the HTML content of the page
                    html = requests.get(url)
                    html.raise_for_status()  # Check for request errors
                    soup = BeautifulSoup(html.content, 'html.parser')
                    
                    # Find the section with the ingredients
                    section = soup.find('section', class_='block text-center')
                    if section:
                        ingredients = []
                        
                        # Extract text from all <p> tags within the section
                        for p in section.find_all('p'):
                            text = p.get_text(strip=True)
                            cleaned_text = re.sub(r'\s+', ' ', text).strip()
                            
                            if cleaned_text:  # Skip empty lines
                                ingredients.append(cleaned_text)
                        
                        # Write ingredients as a list followed by the URL
                        if ingredients:
                            file2.write(f'{ingredients} | {url}\n')
                except Exception as e:
                    print(f"Error processing URL {url}: {e}")

# Run the function
koostisosad()
