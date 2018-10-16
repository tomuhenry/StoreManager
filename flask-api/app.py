from flask import Flask, jsonify, json, request, abort, session
from data_models import products, sales
from datetime import datetime
import os

app = Flask(__name__)

time = str(datetime.now())


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Invalid request/input'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server Error has occured, Check input'}), 500


@app.route('/store-manager/api/v1/')
def home():
    return jsonify({"Welcome": "Welcome to the Store manager api"})

# Add a product to the list


@app.route('/store-manager/api/v1/admin/products', methods=['POST'])
def add_product():
    data = request.json

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
            "product_id": products[-1]['product_id']+1,
            "product_category": product_category,
            "product_name": product_name,
            "product_specs": product_specs,
            "product_stock": product_stock,
            "product_price": product_price,
        }
        products.append(product)
        return jsonify({"Success": "The product '{0}' has been added".format(product["product_name"])}), 200


@app.route('/store-manager/api/v1/admin/products', methods=['GET'])
def view_all_products():
    return jsonify({"Products": products}), 200


@app.route('/store-manager/api/v1/admin/products/<int:product_id>', methods=['GET'])
def view_one_product(product_id):
    product = [
        product for product in products if product["product_id"] == product_id]

    if len(product) == 0:
        abort(500)

    return jsonify({"Product": product[0]}), 200


@app.route('/store-manager/api/v1/admin/products/<int:product_id>', methods=['DELETE'])
def delete_a_product(product_id):
    product = [
        product for product in products if product["product_id"] == product_id]

    if len(product) == 0:
        abort(500)

    products.remove(product[0])
    return jsonify({"Deleted": 
    "Product {0} was deleted successfully".format(product[0]["product_name"])}), 200

@app.route('/store-manager/api/v1/admin/sales', methods=['POST'])
@app.route('/store-manager/api/v1/user/sales', methods=['POST'])
def add_sales():
    data = request.json

    product_id = data['product_id']
    sale_quantity = data['sale_quantity']
    unit_price = data['sale_price']

    if type(sale_quantity) != int and type(unit_price) != int and type(product_id):
        abort(400)

    elif not data or data == "":
        abort(400)

    else:
        product = [
        product for product in products if product["product_id"] == product_id]
        product[0]["product_stock"] = product[0]["product_stock"] - sale_quantity

        if len(product) == 0:
            abort(500)
        
        sale = {
            "sale_id": sales[-1]["sale_id"]+1,
            "product_id": product_id,
            "sale_quantity": sale_quantity,
            "unit_price": unit_price,
            "sale_price": unit_price * sale_quantity,
            "date_sold": time
        }
        sales.append(sale)
        return jsonify({"Success": 
            " {0} of {1} has been sold worth {2}".format(sale["sale_quantity"], 
            product[0]["product_name"], sale["sale_price"])}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)
