import  sqlite3 as lite
import sys

sales = (
    ('Janez', 125000),
    ('Makro', 255000),
    ('Metka', 256000),
    ('Mojca', 369000),
    ('Alenka', 45800)
)

conn = lite.connect('sales.db')

with conn:
    cur = conn.cursor()

    cur.execute('DROP TABLE  IF EXISTS reps')
    cur.execute('CREATE TABLE reps(name TEXT, amount FLOAT)')
    cur.executemany('INSERT INTO reps VALUES(?, ?)', sales)