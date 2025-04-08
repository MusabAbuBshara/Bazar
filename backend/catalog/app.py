from flask import Flask
import sqlite3

// Setting up the database path for the catalog service in data folder.
app = Flask(__name__)
DATABASE = '/data/catalog.db'

// Establishing a connection to an SQLite database to store the catalog data.
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn