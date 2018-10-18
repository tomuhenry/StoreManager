from flask import Flask, jsonify, json, request, abort, session
from api.endpoints.functions import Products, Sales, sales, products

app = Flask(__name__)

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


@app.route('/store-manager/api/v1/admin/products', methods=['POST'])
def add_product():
    data = request.json

    product_category = data['product_category']
    product_name = data['product_name']
    product_specs = data['product_specs']
    product_stock = data['product_stock']
    product_price = data['product_price']

    product_cls = Products(product_category, product_name,
                           product_specs, product_stock, product_price)

    if product_cls.add_product() is True:
        return jsonify({"Success": "The product has been added"})

    else:
        return jsonify({"Duplicate": "The product already exits"})


@app.route('/store-manager/api/v1/admin/products', methods=['GET'])
def view_all_products():
    return jsonify({"Products": products})


@app.route('/store-manager/api/v1/admin/products/<int:product_id>', methods=['GET'])
def view_one_product(product_id):
    product = [
        product for product in products if product["product_id"] == product_id]

    if len(product) == 0:
        abort(404)

    return jsonify({"Product": product[0]})


@app.route('/store-manager/api/v1/admin/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    data = request.json

    try:

        product_stock = int(data['product_stock'])
        product_price = int(data['product_price'])

        product = [
            product for product in products if product["product_id"] == product_id]

        if len(product) == 0:
            abort(500)

        else:
            product[0]["product_stock"] = product_stock
            product[0]["product_price"] = product_price

            return jsonify({"Updated":
                            "Product {0} was updated successfully".format(product[0]["product_name"])})

    except:
        abort(500)


@app.route('/store-manager/api/v1/admin/products/<int:product_id>', methods=['DELETE'])
def delete_a_product(product_id):
    product = [
        product for product in products if product["product_id"] == product_id]

    if len(product) == 0:
        abort(404)

    products.remove(product[0])
    return jsonify({"Deleted":
                    "Product {0} was deleted successfully".format(product[0]["product_name"])})


@app.route('/store-manager/api/v1/admin/sales', methods=['POST'])
@app.route('/store-manager/api/v1/user/sales', methods=['POST'])
def add_sales():
    data = request.json

    product_id = data['product_id']
    sale_quantity = data['sale_quantity']
    unit_price = data['sale_price']

    sale_cls = Sales(product_id, sale_quantity, unit_price)

    if type(sale_quantity) != int and type(unit_price) != int and type(product_id):
        abort(400)

    elif not data or data == "":
        abort(400)

    elif sale_cls.add_sale() is True:
        return jsonify({"Success": "The sale item has been added"})

    else:
        return jsonify({"Out of Stock": "Sorry, Not enough items in stock"})


@app.route('/store-manager/api/v1/admin/sales', methods=['GET'])
def get_all_records():
    return jsonify({"Sales": sales})


@app.route('/store-manager/api/v1/admin/sales/<int:sale_id>', methods=['GET'])
def view_one_record(sale_id):
    sale = [
        sale for sale in sales if sale["sale_id"] == sale_id]

    if len(sale) == 0:
        abort(404)

    return jsonify({"Sale": sale[0]})


if __name__ == '__main__':
    app.run(debug=True, port=8080)