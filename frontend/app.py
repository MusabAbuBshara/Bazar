from flask import Flask , jsonify
import os
import requests

# Setting up CATALOG_SERVER and ORDER_SERVER for servving the catalog and order services.
app = Flask(__name__)
CATALOG_URL = os.getenv('CATALOG_SERVER', 'http://catalog:5001')
ORDER_URL = os.getenv('ORDER_SERVER', 'http://order:5002')

# Endpoint to request to get books by topic from catalog server.
@app.route('/search/<topic>', methods=['GET'])
def search(topic):
    try:
        response = requests.get(f'{CATALOG_URL}/search/{topic}', timeout=3)
        response.raise_for_status()
        return jsonify({'results': response.json()}), 200
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Catalog service unavailable'}), 503

# Endpoint to request to get book details by item_id from catalog server.
@app.route('/info/<int:item_id>', methods=['GET'])
def info(item_id):
    try:
        response = requests.get(f'{CATALOG_URL}/info/{item_id}', timeout=3)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Catalog service unavailable'}), 503

# Endpoint to request to purchase a book from order server.
@app.route('/purchase/<int:item_id>', methods=['POST'])
def purchase(item_id):
    try:
        response = requests.post(f'{ORDER_URL}/purchase/{item_id}', timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Order service unavailable'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)