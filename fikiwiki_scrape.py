import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import string
from tqdm import tqdm
import time

letter = 'A'

def scrape_letter(letter):
    r = requests.get(f'https://en.wikipedia.org/wiki/List_of_acronyms:_{letter}')
    soup = BeautifulSoup(r.text).body
    li = soup.find_all('li')
    acros = [l.text for l in li if '–' in l.text]
    return acros

acronyms = []
for letter in tqdm(string.ascii_uppercase):
    a = scrape_letter(letter)
    acronyms.extend(a)
    time.sleep(1)

df = pd.DataFrame(acronyms)
df['acronym'], df['definition'] = df[0].str.split(' – ', 1).str
df = df.dropna(subset=['definition'])
df['definition'] = df['definition'].apply(lambda x: re.sub('^(.*?)\s', '', x))
df['definition'] = df['definition'].apply(lambda x: re.sub('\(.*$', '', x))

df['a_len'] = [len(a) for a in df.acronym]
df['d_len'] = [len(d.strip().split(' ')) for d in df.definition]
df = df[(df['a_len'] == df['d_len']) & (df['a_len'] >= 3)]
df = df.reset_index(drop=True)
df = df[['acronym', 'definition']]

df.to_csv('data/acronyms.csv', index=False)
