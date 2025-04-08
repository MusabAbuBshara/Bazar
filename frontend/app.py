from flask import Flask
import os

// Setting up CATALOG_SERVER and ORDER_SERVER for servving the catalog and order services.
app = Flask(__name__)
CATALOG_URL = os.getenv('CATALOG_SERVER', 'http://catalog:5001')
ORDER_URL = os.getenv('ORDER_SERVER', 'http://order:5002')

