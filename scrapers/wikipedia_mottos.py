import re
import sqlite3
import requests
from bs4 import BeautifulSoup

# extract
url = 'https://en.wikipedia.org/wiki/List_of_mottos'
html = requests.get(url).text
soup = BeautifulSoup(html)
li = soup.find_all('li')

# transform
x = [l.text for l in li if ':' in l.text]
x = [re.sub('\[{0-9}{1,2,3}\]', '', xi) for xi in x]
x = [xi.split(':', 1) for xi in x]
x = [xi for xi in x if len(xi) == 2]
items = [(xi[0].strip(), xi[1].strip()) for xi in x]

# load
con = sqlite3.connect('data/categories.db')
c = con.cursor()
c.execute('CREATE TABLE mottos (prompt TEXT, answer TEXT, flag INT)')
c.executemany('INSERT INTO mottos VALUES (?,?,0)', items)
con.commit()
con.close()
