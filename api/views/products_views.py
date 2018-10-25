from flask import Flask, jsonify, json, request, abort, Blueprint
from api.views.functions import Products, products

prod = Blueprint('prod',__name__)

@prod.route('/products', methods=['POST'])
def add_product():
    data = request.json

    product_name = data['product_name']
    product_specs = data['product_specs']
    product_stock = data['product_stock']
    product_price = data['product_price']
    
    if product_name is "" or product_price is "" or not product_stock:
        abort(400)


    product_cls = Products(product_name, product_specs,
                           product_stock, product_price)

    prod_values = [product_name, product_price, product_specs, product_stock]

    dup_product = [product for product in products if set(
        prod_values).issubset(product.values())]

    if len(dup_product) > 0:
        return jsonify({"Duplicate": "The product already exits"}), 200

    product_cls.add_product()
    return jsonify({"Success": "The product has been added"}), 200


@prod.route('/products', methods=['GET'])
def view_all_products():
    return jsonify({"Products": products})


@prod.route('/products/<int:product_id>', methods=['GET'])
def view_one_product(product_id):
    product = [
        product for product in products if ('product_id', product_id) in product.items()]

    if len(product) is 0:
        abort(404)

    else:
        return jsonify({"Product": product}), 200


@prod.route('/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    data = request.json

    product_stock = int(data['product_stock'])
    product_price = int(data['product_price'])

    product = [
        product for product in products if product["product_id"] == product_id]

    if len(product) == 0:
        return jsonify({"Unknown": "There is not product with ID '{0}' in the system ".format(product_id)}), 200

    else:
        product[0]["product_stock"] = product_stock
        product[0]["product_price"] = product_price

        return jsonify({"Updated":
                        "Product {0} was updated successfully".format(product[0]["product_name"])}), 200


@prod.route('/products/<int:product_id>', methods=['DELETE'])
def delete_a_product(product_id):
    product = [
        product for product in products if product["product_id"] == product_id]

    if len(product) == 0:
        abort(404)

    products.remove(product[0])
    return jsonify({"Deleted":
                    "Product {0} was deleted successfully".format(product[0]["product_name"])})

