import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape_letter_links(letter_index):
    url = f'https://www.ikea.com/us/en/catalog/productsaz/{letter_index}/'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text).body
    products = soup.find_all('li', {'class': 'productsAzLink'})
    links = ['http://www.ikea.com' + p.a['href'] for p in products]
    links = [l for l in links if 'collections' not in l]
    return links

def scrape_series_page(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.text).body
    product = soup.find('div', {'class': 'categoryGray'}).text
    description = soup.find('h2', {'class': 'headOneGray'}).text
    details = soup.find('p', {'class': 'bodyTextGray'}).text
    return product, description, details

all_links = []
for i in tqdm(range(26)):
    links = scrape_letter_links(i)
    all_links.extend(links)
    time.sleep(1)

products = []
for link in tqdm(all_links):
    try:
        product = scrape_series_page(link)
        products.append(product)
    except AttributeError:
        pass
    time.sleep(1)

import pandas as pd

products






#
