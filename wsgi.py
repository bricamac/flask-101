from flask import Flask, jsonify
app = Flask(__name__)

PRODUCTS = [
    {'id': 1, 'name': 'Skello'},
    {'id': 2, 'name': 'Socialive.tv'},
    {'id': 3, 'name': 'coca'}
]

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def firstjson():
    return jsonify(PRODUCTS)

@app.route('/api/v1/products/<int:product_id>')
def readproduct(product_id):

    for product in PRODUCTS:
        if product['id'] == product_id:
            # Product found...
            return jsonify(product)
    # Production not found
    return jsonify({'ERROR': 'product not found'}), 404


