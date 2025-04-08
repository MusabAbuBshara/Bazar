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

# Response to return book details by item_id to the frontend request.
@app.route('/info/<int:item_id>', methods=['GET'])
def info(item_id):
    conn = get_db()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    return jsonify(dict(book)) if book else ('Not Found', 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)