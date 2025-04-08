from flask import Flask
import sqlite3

// Setting up the database path for the order service in data folder.
app = Flask(__name__)
DATABASE = '/data/order.db'
CATALOG_URL = os.getenv('CATALOG_SERVER', 'http://catalog:5001')

// Establishing a connection to an SQLite database to store the order data.
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn