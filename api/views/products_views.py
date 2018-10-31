from flask import jsonify, request, abort, Blueprint
from api.models.products import Products
from flask_jwt_extended import jwt_required

prodbp = Blueprint('prod', __name__)

@prodbp.route('/products', methods=['POST'])
# @jwt_required
def add_product():
    data = request.json

    category = data['category']
    product_name = data['product_name']
    product_specs = data['product_specs']
    product_stock = int(data['product_stock'])
    product_price = int(data['product_price'])

    if not product_name or not product_price or not product_stock:
        abort(400)
    
    product_cls = Products()
    product_cls.add_product(category, product_name,
                            product_specs, product_price, product_stock)

    return jsonify({"Success": "The product has been added"}), 201


@prodbp.route('/products', methods=['GET'])
# @jwt_required
def view_all_products():
    product_cls = Products()
    return jsonify({"Products":product_cls.get_all_products()})


@prodbp.route('/products/<int:product_id>', methods=['GET'])
# @jwt_required
def view_one_product(product_id):
    product_cls = Products()
    return jsonify({"Product":product_cls.get_one_product_by_id(product_id)}), 200


@prodbp.route('/products/<product_id>', methods=['DELETE'])
# @jwt_required
def delete_a_product(product_id):
    product_cls = Products()
    product_cls.delete_a_product(product_id)
    return jsonify({"Deleted":"Product was deleted successfully"}), 200

@prodbp.route('/products/<product_id>', methods=['PUT'])
# @jwt_required
def edit_product(product_id):
    data = request.json

    product_stock = int(data['product_stock'])
    product_price = int(data['product_price'])
    product_cls = Products()
    product_cls.edit_a_product(product_id, product_stock, product_price)

    return jsonify({"Updated":
                    "Product was updated successfully"}), 200