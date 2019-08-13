import sqlite3

con = sqlite3.connect('data/fiki.db')
cur = con.cursor()

sql = '''
CREATE TABLE cards (
    id INTEGER PRIMARY KEY,
    prompt TEXT,
    answer TEXT,
    date_created DATE,
    flag INTEGER
);
'''

cur.execute(sql)
con.commit()
con.close()
