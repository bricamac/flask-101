#from copy import deepcopy
from flask import Flask, jsonify,request
app = Flask(__name__)


INITIAL_PRODUCTS = [
    { 'id': 1, 'name': 'Skello' },
    { 'id': 2, 'name': 'Socialive.tv' },
    { 'id': 3, 'name': 'coca'}
]

PRODUCTS = INITIAL_PRODUCTS.copy()

#Pour les tests....
def init_product():
    PRODUCTS.clear()
    PRODUCTS.extend(INITIAL_PRODUCTS)

#Getion d'un IP automatique...
class Counter:
    def __init__(self):
        self.id = 3

    def next(self):
        self.id += 1
        return self.id

app_id=Counter()

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def firstjson():
    return jsonify(PRODUCTS)


@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def read_product(product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            # Product found...
            return jsonify(product)
                # Production not found
    return jsonify({'ERROR': 'product not found'}), 404

@app.route('/api/v1/products/<int:product_id>' , methods=['DELETE'])
def delete_product(product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            # Product found...
            PRODUCTS.remove(product)
            return "", 204
    # Production not found
    return jsonify({'ERROR': 'product not found'}), 404

@app.route('/api/v1/products' , methods=['POST'])
def create_product():
    content = request.json

    #Format des datas...
    if "name" not in content:
        return jsonify({'ERROR': 'input data error'}), 422
    if content["name"] == "" :
        return jsonify({'ERROR': 'input data error'}), 422

    #prochain ID
    app_id.next()
    #ajout element
    PRODUCTS.append({'id':app_id.id,'name':content["name"]})
    return jsonify({'id':app_id.id }),201


@app.route('/api/v1/products/<int:product_id>' , methods=['PATCH'])
def update_product(product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            # Product found...
            content = request.json
            #Format des datas...
            if "name" not in content:
                return jsonify({'ERROR': 'input data error'}), 422
            if content["name"] == "" :
                return jsonify({'ERROR': 'input data error'}), 422

            product["name"] = content["name"]
            return "", 204

    # Production not found
    return jsonify({'ERROR': 'product not found'}), 404


