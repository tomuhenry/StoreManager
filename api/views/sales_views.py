from flask import jsonify, request, abort, Blueprint

salebp = Blueprint('salebp',__name__)

# @salebp.route('/user/sales', methods=['POST'])
# def add_sales():
#     data = request.json

#     product_id = data['product_id']
#     sale_quantity = data['sale_quantity']

#    pass


# @salebp.route('/admin/sales', methods=['GET'])
# def get_all_records():
#     pass

# @salebp.route('/admin/sales/<sale_id>', methods=['GET'])
# def view_one_record(sale_id):
#     pass