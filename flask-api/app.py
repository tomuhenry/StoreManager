from flask import Flask, jsonify, json, request, abort
from data_models import products, sales
from datetime import datetime

app = Flask(__name__)

time = str(datetime.now())

@app.errorhandler(404)             
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)             
def bad_request(error):
    return jsonify({'error': 'Invalid request/input'}), 400

@app.route('/store-manager/api/v1/')
def home():
   return jsonify({"Welcome":"Welcome to the Store manager api"})

@app.route('/store-manager/api/v1/products', methods=['POST'])
def add_product():
    data = request.json
    product_id = products[-1]['product_id']+1,
    product_category = data['product_category']
    product_name = data['product_name']
    product_specs = data['product_specs']
    product_stock = data['product_stock']
    product_price = data['product_price']

    if type(product_stock) != int and type(product_price) != int:
        abort(400)
    
    elif not data or data == "":
        abort(400)

    else:
        product = {
            "product_id": product_id,
            "product_category": product_category,
            "product_name": product_name,
            "product_specs": product_specs,
            "product_stock": product_stock,
            "product_price": product_price,
        }
        products.append(product);
        return jsonify({"Success":"The product {0} has been added".format(product["product_name"])}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)