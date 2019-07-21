import sqlite3
import requests
from bs4 import BeautifulSoup

def scrape(page):
    url = f'https://en.wikipedia.org/wiki/{page}'
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    li = soup.find_all('li')
    return li

def clean(x):
    x = [xi.text for xi in x if ' – ' in xi.text and 'fear/dislike' not in xi.text]
    x = [xi.split(' – ', 1) for xi in x]
    x = [xi for xi in x if len(xi) == 2]
    x = [(xi[0].strip(), xi[1].strip()) for xi in x]
    return x

def download(page):
    return clean(scrape(page))

if __name__ == '__main__':
    con = sqlite3.connect('data/categories.db')
    c = con.cursor()
    c.execute('CREATE TABLE canadians (prompt TEXT, answer TEXT, flag INT)')
    items = download('List_of_Canadians')
    c.executemany('INSERT INTO canadians VALUES (?,?,0)', items)
    con.commit()
    con.close()
