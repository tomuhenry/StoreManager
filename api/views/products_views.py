from flask import jsonify, request, abort, Blueprint
from api.models.products import Products
from flask_jwt_extended import jwt_required
from api.views.user_views import user_check

prodbp = Blueprint('prod', __name__)

product_cls = Products()


@prodbp.route('admin/products', methods=['POST'])
@jwt_required
def add_product():
    data = request.json

    product_name = str(data['product_name'])
    product_specs = str(data['product_specs'])
    product_stock = int(data['product_stock'])
    product_price = int(data['product_price'])
    prod_name = product_name.strip()

    if not prod_name or not product_price or not product_stock:
        abort(400)

    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to perform action"}), 401

    check_dup = product_cls.check_same_product(product_name, product_specs)

    if not check_dup:
        product_cls.add_product(product_name=product_name,
                                product_specs=product_specs,
                                product_price=product_price,
                                product_stock=product_stock)
        return jsonify({"Success": "The product has been added"}), 201

    return jsonify({"Duplicate": "This product is already in the database"}), 200


@prodbp.route('admin/products', methods=['GET'])
def view_all_products():
    return jsonify({"Products": product_cls.get_all_products()}), 200


@prodbp.route('admin/products/<int:product_id>', methods=['GET'])
def view_one_product(product_id):
    product = product_cls.get_one_product_by_id(product_id)
    if not product:
        return jsonify({"Not Found":
                        "The product with ID '{0}' was not found".format(product_id)}), 404

    return jsonify({"Product": product}), 200


@prodbp.route('admin/products/<product_id>', methods=['DELETE'])
@jwt_required
def delete_a_product(product_id):
    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to perform action"}), 401

    if not product_cls.get_one_product_by_id(product_id):
        return jsonify({"Not Found":
                        "The product with ID '{0}' was not found".format(product_id)}), 404
    product_cls.delete_a_product(product_id)
    return jsonify({"Deleted": "Product was deleted successfully"}), 200


@prodbp.route('admin/products/category', methods=['POST'])
@jwt_required
def create_new_category():
    data = request.json
    category_name = data['category_name']

    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to perform action"}), 401

    if product_cls.get_products_by_category(category_name):
        return jsonify({
            "Message": "Category with name '{0}' already exist".format(category_name)})

    product_cls.create_category(category_name)
    return jsonify({"Created": "The '{0}' category has been created"})


@prodbp.route('admin/products/<product_id>', methods=['PUT'])
@jwt_required
def edit_product(product_id):
    data = request.json

    product_name = data['product_name']
    product_stock = int(data['product_stock'])
    product_price = int(data['product_price'])

    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to perform action"}), 401

    if not product_cls.get_one_product_by_id(product_id):
        return jsonify({"Not Found":
                        "The product with ID '{0}' was not found".format(product_id)}), 404

    product_cls.edit_a_product(
        product_id, product_name, product_stock, product_price)

    return jsonify({"Updated":
                    "Product was updated successfully"}), 200


@prodbp.route('category', methods=['POST'])
@jwt_required
def add_category():
    data = request.json

    category_name = data['category_name']
    cat_name = category_name.strip()

    if user_check() is False:
        return jsonify({"Alert": "Only Admin can perform this action"}), 401

    if not cat_name or not category_name:
        abort(400)

    if not product_cls.get_category_by_name(category_name):
        product_cls.create_category(category_name)
        return jsonify({"Great": "New Category '{0}' created successfully".format(category_name)}), 201
    return jsonify({"Duplicate": "Category already exists"}), 200


@prodbp.route('category', methods=['GET'])
@jwt_required
def get_all_categories():
    if user_check() is False:
        return jsonify({"Alert": "Only Admin can perform this action"}), 401

    return jsonify({"categories": product_cls.get_all_categories()})


@prodbp.route('products/category/<product_id>', methods=['PUT'])
@jwt_required
def add_category_to_product(product_id):
    data = request.json

    category_type = int(data['category_type'])

    if user_check() is False:
        return jsonify({"Alert": "Only Admin can perform this action"}), 401

    if not category_type or type(category_type) is not int:
        abort(400)

    if not product_cls.get_one_product_by_id(product_id):
        return jsonify({"Not found": "The product was not found"})

    product_cls.add_category_to_product(product_id, category_type)

    return jsonify({"Added":"The product has been added to the category"})

@prodbp.route('category/<category_id>', methods=['GET'])
@jwt_required
def get_category_by_id(category_id):
    if user_check() is False:
        return jsonify({"Alert": "Only Admin can perform this action"}), 401
    
    my_category = product_cls.get_category_by_id(category_id)

    if not my_category:
        return jsonify({"Not found": "The product was not found"})
    return jsonify({"Category": my_category})

@prodbp.route('products/category/<category_type>', methods=['GET'])
@jwt_required
def get_products_by_category(category_type):

    if user_check() is False:
        return jsonify({"Alert": "Only Admin can perform this action"}), 401

    if not product_cls.get_category_by_id(category_type):
        return jsonify({"Not found": "The category was not found"})

    get_products = product_cls.get_products_by_category(category_type)

    return jsonify({"Products":get_products})
