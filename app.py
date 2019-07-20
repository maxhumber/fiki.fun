import pandas as pd
import flask

app = flask.Flask(__name__)
df = pd.read_csv('data/acronyms.csv')

@app.route('/')
def get_random():
    a, d = df.sample().values.tolist()[0]
    return f'<h1>{a}</h1><br><h3>{d}</h3>'

if __name__ == '__main__':
    app.run()
