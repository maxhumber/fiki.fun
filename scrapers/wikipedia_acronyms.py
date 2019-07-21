import re
import sqlite3
import string
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def parse_li(x):
    if len(x) == 2:
        return x.text
    else:
        split = x.text.split('\n')
        acro = split[0]
        acros = [f'{acro} – {d}' for d in split[1:]]
        return acros

def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

def scrape_letter(letter):
    r = requests.get(f'https://en.wikipedia.org/wiki/List_of_acronyms:_{letter}')
    soup = BeautifulSoup(r.text).body
    li = soup.find_all('li')
    nested = [parse_li(l) for l in li]
    acronyms = flatten(nested)
    return acronyms

def scape_all_letters():
    acronyms = []
    for letter in tqdm(string.ascii_uppercase):
        a = scrape_letter(letter)
        acronyms.extend(a)
        time.sleep(1)
    return acronyms

if __name__ == '__main__':
    # extract
    acronyms = scape_all_letters()
    # transform
    x = acronyms.copy()
    x = [xi.split(' – ', 1) for xi in x]
    x = [xi for xi in x if len(xi) == 2]
    x = [[xi[0].strip(), xi[1].strip()] for xi in x if 2 < len(xi[0]) <= 5]
    x = [[xi[0], re.sub('^\(.*?\)\s', '', xi[1])] for xi in x]
    x = [(xi[0], xi[1].split(' (')[0]) for xi in x]
    items = [xi for xi in x if len(xi[0]) == len(xi[1].split(' '))]
    # load
    con = sqlite3.connect('data/categories.db')
    c = con.cursor()
    c.execute('CREATE TABLE acronyms (prompt TEXT, answer TEXT, flag INT)')
    c.executemany('INSERT INTO acronyms VALUES (?,?,0)', items)
    con.commit()
    con.close()
