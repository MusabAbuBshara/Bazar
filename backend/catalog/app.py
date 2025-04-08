from flask import Flask, jsonify, request
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

# update the stock of a book by item_id to the frontend request.
@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    data = request.get_json()
    if not data or 'field' not in data or 'amount' not in data:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400
    
    field = data['field']
    amount = data['amount']
    
    if field not in ['quantity', 'price']:
        return jsonify({'success': False, 'error': 'Invalid field'}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f'UPDATE books SET {field} = {field} + ? WHERE id = ?',
            (amount, item_id)
        )
        success = cursor.rowcount > 0
        conn.commit()
        return jsonify({'success': success})
    except sqlite3.Error as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)