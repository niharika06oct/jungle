from flask import Flask, render_template, jsonify
import os
import logging
import sys

app = Flask(__name__)

# Configure logging to use stdout only for Android logcat
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Sample product data (in a real app, this would come from a database)
products = [
    {
        "id": 1,
        "name": "Bamboo Toothbrush",
        "price": 4.99,
        "description": "Eco-friendly bamboo toothbrush",
        "image": "bamboo_toothbrush.jpg",
        "category": "Personal Care"
    },
    {
        "id": 2,
        "name": "Reusable Produce Bags",
        "price": 12.99,
        "description": "Set of 5 mesh produce bags",
        "image": "produce_bags.jpg",
        "category": "Kitchen"
    },
    # Add more products as needed
]

@app.route('/')
def home():
    app.logger.info('Handling request for home page')
    try:
        app.logger.debug('Rendering template with %d products', len(products))
        return render_template('index.html', products=products)
    except Exception as e:
        app.logger.error('Error rendering home page: %s', str(e))
        return f"Error: {str(e)}", 500

@app.route('/api/products')
def get_products():
    app.logger.info('Handling request for products API')
    return jsonify(products)

def run_server():
    app.logger.info('Starting Flask server...')
    try:
        # Use 0.0.0.0 to allow connections from the Android WebView
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        app.logger.error('Error starting server: %s', str(e))
        raise

if __name__ == '__main__':
    run_server() 