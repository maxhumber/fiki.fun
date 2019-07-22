import sqlite3
import flask
from flask import render_template, url_for, abort

app = flask.Flask(__name__)
con = sqlite3.connect('data/categories.db', check_same_thread=False)
c = con.cursor()

tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [table[0] for table in tables.fetchall()]

@app.route('/')
def index():
    return render_template('index.html', categories=tables)

@app.route('/c/<category>')
def fetch_prompt(category):
    if category.lower() not in tables:
        abort(400)
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
