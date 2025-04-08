from flask import Flask, jsonify, request
import sqlite3
import requests
import os

# Setting up the database path for the order service in data folder.
app = Flask(__name__)
DATABASE = '/data/order.db'
CATALOG_URL = os.getenv('CATALOG_SERVER', 'http://catalog:5001')

# Establishing a connection to an SQLite database to store the order data.
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/purchase/<int:item_id>', methods=['POST'])
def purchase(item_id):
    try:
        # Atomic stock decrement
        response = requests.post(
            f'{CATALOG_URL}/update/{item_id}',
            json={'field': 'quantity', 'amount': -1},
            timeout=5
        )
        response.raise_for_status()
        
        if not response.json().get('success'):
            return jsonify({'success': False, 'error': 'Out of stock'}), 200
        
        # Log order
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (item_id) VALUES (?)', (item_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': 'Catalog service unreachable'}), 503
    except sqlite3.Error as e:
        return jsonify({'success': False, 'error': 'Database error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)