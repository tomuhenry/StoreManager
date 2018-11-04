from api.views.user_views import userbp
from api.views.products_views import prodbp
from api.views.sales_views import salebp
from flask import jsonify, Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'SomeRaND0m5eC7eTK3Y'
jwt = JWTManager(app)

app.register_blueprint(prodbp, url_prefix='/store-manager/api/v1')

app.register_blueprint(salebp, url_prefix='/store-manager/api/v1')

app.register_blueprint(userbp, url_prefix='/store-manager/api/v1')

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Invalid request/input'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Information could not be found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'There has been a Server Error'}), 500

@app.errorhandler(TypeError)
def type_error(error):
    return jsonify({'error': 'Type Error has occured'})

@app.errorhandler(ValueError)
def value_error(error):
    return jsonify({'error': 'Wrong Value in the input'})

@app.errorhandler(KeyError)
def key_error(error):
    return jsonify({'error': 'A key error has been detected, check your inputs'})


@app.route('/', methods=['GET'])
def index():
    return jsonify({"Welcome": "Welcome to the Store manager api"})