import pandas as pd
import flask
import json
import random

app = flask.Flask(__name__)
df = pd.read_csv('data/acronyms.csv')
dates = list(json.load(open('data/dates.json', 'r')).items())

# /c/inventors
# /c/acronyms
# /c/dates
# /c/canadians
# /c/phobias
# /c/mottos

@app.route('/c/<category>')



@app.route('/')
def get_random():
    a, d = df.sample().values.tolist()[0]
    return f'<h1>{a}</h1><br><h3>{d}</h3>'

@app.route('/date')
def get_random_date():
    d, e = random.choice(dates)
    return f'<h1>{d}</h1><br><h3>{e}</h3>'

if __name__ == '__main__':
    app.run()
