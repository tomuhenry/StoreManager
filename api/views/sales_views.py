from flask import jsonify, request, abort, Blueprint
from api.views.user_views import user_check
from flask_jwt_extended import get_jwt_identity, jwt_required
from api.models.sales import Sales
from api.views.products_views import product_cls
from datetime import datetime
from api.database.database import Database

salebp = Blueprint('salebp', __name__)

sales_cls = Sales()
database_cls = Database()


@salebp.route('/user/sales', methods=['POST'])
@jwt_required
def add_sales():
    data = request.json

    sale_quantity = int(data['sale_quantity'])
    product_sold = int(data['product_sold'])
    date_sold = datetime.now()

    if not sale_quantity or not product_sold or not product_sold:
        abort(400)

    if user_check() is True:
        return jsonify({"Alert": "Admin cannot make a sale"}), 401

    product = product_cls.get_one_product_by_id(product_sold)

    if not product:
        return jsonify({"Unknown": "The product has not been found"})

    prod_stock = product['product_stock']
    prod_price = product['product_price']

    if sale_quantity > prod_stock or prod_stock == 0:
        return jsonify({"Sorry": "Not enough items in stock"})

    new_stock = prod_stock - sale_quantity

    sale_price = prod_price * sale_quantity

    reduce_stock = """UPDATE products SET product_stock = {0} 
                WHERE product_id = {1} """.format(new_stock, product_sold)

    database_cls.execute_query(reduce_stock)

    sales_cls.make_a_sale(sale_quantity, sale_price, date_sold, product_sold)

    return jsonify({"Success": "The Sale has been made"}), 201
