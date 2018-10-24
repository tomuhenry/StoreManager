from flask import Flask, jsonify, json, request, abort, redirect, Blueprint
from api.endpoints.functions import Products, Sales, sales, products, Users, users
import werkzeug.exceptions

app = Flask(__name__)

store = Blueprint('store', __name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Invalid request/input'}), 400


@app.errorhandler(TypeError)
def type_error(error):
    return jsonify({'error': 'Wrong input type'})


@app.errorhandler(ValueError)
def value_error(error):
    return jsonify({'error': 'Wrong Value in the input'})

@app.errorhandler(KeyError)
def key_error(error):
    return jsonify({'error': 'A key error has been detected, check your inputs'})


@app.route('/', methods=['GET'])
def index():
    return jsonify({"Welcome": "Welcome to the Store manager api"})


@app.route('/store-manager/api/v1/signup', methods=['POST'])
def register_user():
    data = request.json

    email = data['email']
    name = data['name']
    password = data['password']
    rights = data['rights']

    if not email or not name or not password or not rights:
        abort(400)

    user_cls = Users(email, name, password, rights)

    if user_cls.validate_email() is False:
        return jsonify({"Error": "Invalid email"})

    if user_cls.check_duplicate() is False:
        return jsonify({"Failed": "User with email '{0}' already exists".format(email)})

    user_cls.add_user()
    return jsonify({"Success": "User with name '{0}' has been added".format(name)})


@app.route('/store-manager/api/v1/login', methods=['POST'])
def user_login():
    data = request.json

    email = data['email']
    password = data['password']

    if not email or not password:
        abort(400)

    user_cls = Users(email, " name", password, "rights")

    if user_cls.user_login() is True:
        return jsonify({"Success": "User Logged in successfuly"}), 200

    else:
        return jsonify({"Failure": "Wrong login information"}), 200


@app.route('/store-manager/api/v1/users', methods=['GET'])
def get_all_users():
    return jsonify({"Users": users}), 200


@app.route('/store-manager/api/v1/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = [user for user in users if user_id in user.values()]
    if len(user) == 0:
        return jsonify({"Not Found": "No user with ID '{0}' in the database".format(user_id)}), 200

    else:
        return jsonify({"User": user}), 200


@app.route('/store-manager/api/v1/admin/products', methods=['POST'])
def add_product():
    data = request.json

    product_name = data['product_name']
    product_specs = data['product_specs']
    product_stock = data['product_stock']
    product_price = data['product_price']
    
    if not product_name or not product_price or not product_stock or not product_specs:
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


@app.route('/store-manager/api/v1/admin/products', methods=['GET'])
def view_all_products():
    return jsonify({"Products": products}), 200


@app.route('/store-manager/api/v1/admin/products/<int:product_id>', methods=['GET'])
def view_one_product(product_id):
    product = [
        product for product in products if ('product_id', product_id) in product.items()]

    if len(product) is 0:
        abort(404)

    else:
        return jsonify({"Product": product}), 200


@app.route('/store-manager/api/v1/admin/products/<int:product_id>', methods=['PUT'])
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

    product = [
        product for product in products if product["product_id"] == product_id]

    if len(product) < 1:
        abort(404)

    product_price = product[0]['product_price']

    sale_cls = Sales(product_id, sale_quantity, product_price)

    if sale_quantity > product[0]["product_stock"]:
        return jsonify({"Out of Stock": "Sorry, Not enough items in stock"})

    else:
        product[0]["product_stock"] -= sale_quantity

    sale_cls.add_sale()
    return jsonify({"Success": "The sale item has been added"})


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
