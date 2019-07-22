import sqlite3
import flask
from flask import render_template, url_for

app = flask.Flask(__name__)
con = sqlite3.connect('data/categories.db', check_same_thread=False)
c = con.cursor()

@app.route('/')
def index():
    r = c.execute('''
        SELECT
        name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY random()
    ''')
    cats = r.fetchall()
    categories = [c[0] for c in cats]
    # TODO: make this dynamic again
    return render_template('index.html', categories=categories)

@app.route('/c/<category>')
def fetch_prompt(category):
    # TODO: fix sql injection lol
    c.execute(f'''
        SELECT
        prompt,
        answer
        FROM {category}
        ORDER BY RANDOM()
        LIMIT 1''')
    prompt, answer = c.fetchone()
    return render_template('prompt.html', prompt=prompt, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
