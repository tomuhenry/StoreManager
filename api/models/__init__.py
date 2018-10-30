from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'SomeRaND0m5eC7eTK3Y'
jwt = JWTManager(app)
