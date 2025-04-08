import sqlite3

DATABASE = '/data/catalog.db'

books = [
    (1, 'How to get a good grade in DOS in 40 minutes a day', 'distributed systems', 10, 50.0),
    (2, 'RPCs for Noobs', 'distributed systems', 5, 40.0),
    (3, 'Xen and the Art of Surviving Undergraduate School', 'undergraduate school', 8, 45.0),
    (4, 'Cooking for the Impatient Undergrad', 'undergraduate school', 7, 35.0),
]

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')

cursor.executemany('INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?, ?)', books)
conn.commit()
conn.close()
