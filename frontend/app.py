from flask import Flask, jsonify
import os
import requests
from cachetools import TTLCache, keys
from functools import wraps
import time

# Setting up CATALOG_SERVER and ORDER_SERVER for servving the catalog and order services.
app = Flask(__name__)
CATALOG_URL = os.getenv('CATALOG_SERVER', 'http://catalog:5001')
ORDER_URL = os.getenv('ORDER_SERVER', 'http://order:5002')

# Configure caches with a 30-second TTL
SEARCH_CACHE = TTLCache(maxsize=100, ttl=30)  # Cache for search results
INFO_CACHE = TTLCache(maxsize=1000, ttl=30)   # Cache for book info

def invalidate_caches():
    """Invalidate all caches after a purchase"""
    SEARCH_CACHE.clear()
    INFO_CACHE.clear()

def cache_key(*args, **kwargs):
    """Generate a cache key from the function arguments"""
    return keys.hashkey(*args, **kwargs)

# Endpoint to request to get books by topic from catalog server.
@app.route('/search/<topic>', methods=['GET'])
def search(topic):
    # Check cache first
    cache_key_val = cache_key(topic)
    cached_result = SEARCH_CACHE.get(cache_key_val)
    if cached_result is not None:
        return jsonify({'results': cached_result, 'cache_hit': True}), 200

    try:
        response = requests.get(f'{CATALOG_URL}/search/{topic}', timeout=3)
        response.raise_for_status()
        result = response.json()
        # Cache the result
        SEARCH_CACHE[cache_key_val] = result
        return jsonify({'results': result, 'cache_hit': False}), 200
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Catalog service unavailable'}), 503

# Endpoint to request to get book details by item_id from catalog server.
@app.route('/info/<int:item_id>', methods=['GET'])
def info(item_id):
    # Check cache first
    cache_key_val = cache_key(item_id)
    cached_result = INFO_CACHE.get(cache_key_val)
    if cached_result is not None:
        return jsonify({'data': cached_result, 'cache_hit': True}), 200

    try:
        response = requests.get(f'{CATALOG_URL}/info/{item_id}', timeout=3)
        if response.status_code == 200:
            result = response.json()
            # Cache the result
            INFO_CACHE[cache_key_val] = result
            return jsonify({'data': result, 'cache_hit': False}), 200
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Catalog service unavailable'}), 503

# Endpoint to request to purchase a book from order server.
@app.route('/purchase/<int:item_id>', methods=['POST'])
def purchase(item_id):
    try:
        response = requests.post(f'{ORDER_URL}/purchase/{item_id}', timeout=5)
        if response.status_code == 200:
            # Invalidate caches after successful purchase
            invalidate_caches()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Order service unavailable'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)