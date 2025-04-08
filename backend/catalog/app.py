from flask import Flask , jsonify
import sqlite3

# Setting up the database path for the catalog service in data folder.
app = Flask(__name__)
DATABASE = '/data/catalog.db'

# Establishing a connection to an SQLite database to store the catalog data.
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Response to return books by topic to the frontend request.
@app.route('/search/<topic>', methods=['GET'])
def search(topic):
    conn = get_db()
    books = conn.execute('SELECT id, title FROM books WHERE topic = ?', (topic,)).fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])
