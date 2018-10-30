from flask import Flask, jsonify
from api.views.user_views import app, userbp
from api.views.products_views import prod
from api.views.sales_views import salebp

app.register_blueprint(prod, url_prefix='/store-manager/api/v1/admin')

app.register_blueprint(salebp, url_prefix='/store-manager/api/v1')

app.register_blueprint(userbp, url_prefix='/store-manager/api/v1')


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
