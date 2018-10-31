from flask import jsonify, request, abort, Blueprint

salebp = Blueprint('salebp',__name__)

@salebp.route('/admin/sales', methods=['POST'])
@salebp.route('/user/sales', methods=['POST'])
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


@salebp.route('/admin/sales', methods=['GET'])
def get_all_records():
    return jsonify({"Sales": sales})


@salebp.route('/admin/sales/<sale_id>', methods=['GET'])
def view_one_record(sale_id):
    sale = [
        sale for sale in sales if ('sale_id', sale_id) in sale.items()]

    if len(sale) == 0:
        abort(404)

    else:
        return jsonify({"Sale": sale}), 200
    # sale = [
    #     sale for sale in sales if sale_id in sale.values()]

    # if len(sale) == 0 :
    #     abort(404)

    # return jsonify({"Sale": sale})
