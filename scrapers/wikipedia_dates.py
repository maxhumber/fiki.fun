import calendar
import re
import time
import json
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
    r = requests.get(f'http://en.wikipedia.org/wiki/{date}')
    html = r.text
    m = re.search(r'<span class="mw-headline" id="Events">Events</span>.*?<span class="mw-headline" id="Births">Births</span>', html, re.DOTALL)
    s = m.start()
    e = m.end() - len('<span class="mw-headline" id="Births">Births</span>')
    target_html = html[s:e]
    soup = BeautifulSoup(target_html)
    li = soup.find_all('li')
    events = [f'{day} {month}, {l.text}' for l in li]
    return events

def clean_events(events):
    ev = [e for e in events if ':' not in e]
    ev = [e.split(' – ', 1) for e in ev]
    ev = [s for s in ev if len(s) == 2]
    ev = {date.strip(): event.strip() for date, event in ev}
    return ev

if __name__ == '__main__':
    days = generate_days(2020)
    events = []
    for date in tqdm(days):
        e = scrape_date(date)
        events.extend(e)
        time.sleep(0.5)
    events = clean_events(events)
    with open('data/dates.json', 'w') as f:
        json.dump(events, f, indent=4)
