import calendar
import re
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def generate_days(year=2020):
    month_length = []
    months = list(calendar.month_name)[1:]
    for i, month in enumerate(months):
        days = calendar.monthrange(year, i+1)[1]
        month_length.append((month, days))
    month_and_days = []
    for month, days in month_length:
        for day in range(1, days + 1):
            month_and_days.append((month, str(day)))
    strings = ['_'.join(mad) for mad in month_and_days]
    return strings

def scrape_date(date):
    day, month = date.split('_')
    html = requests.get(f'http://en.wikipedia.org/wiki/{date}').text
    m = re.search(r'<span class="mw-headline" id="Events">Events</span>.*?<span class="mw-headline" id="Births">Births</span>', html, re.DOTALL)
    s = m.start()
    e = m.end() - len('<span class="mw-headline" id="Births">Births</span>')
    soup = BeautifulSoup(html[s:e])
    li = soup.find_all('li')
    events = [f'{day} {month}, {l.text}' for l in li]
    return events

def scrape_all():
    days = generate_days(2020)
    events = []
    for date in tqdm(days):
        e = scrape_date(date)
        events.extend(e)
        time.sleep(0.5)
    return events

if __name__ == '__main__':
    events = scrape_all()
    # transform
    x = events.copy()
    x = [xi.split(' – ', 1) for xi in x]
    x = [xi for xi in x if len(xi) == 2]
    items = [(xi[0].strip(), xi[1].strip()) for xi in x]
    # load
    con = sqlite3.connect('data/categories.db')
    c = con.cursor()
    c.execute('CREATE TABLE dates (prompt TEXT, answer TEXT, flag INT)')
    c.executemany('INSERT INTO dates VALUES (?,?,0)', items)
    con.commit()
    con.close()
