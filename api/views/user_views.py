from flask import jsonify, request, abort, Blueprint, session, Flask
from api.models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (jwt_required, create_access_token,
    get_jwt_identity)
from validate_email import validate_email
from datetime import timedelta

userbp = Blueprint('userbp', __name__)

@userbp.route('/auth/signup', methods=['POST'])
# @jwt_required
def register_user():
    data = request.json

    email = data['email']
    name = data['name']
    password = generate_password_hash(data['password'], method='sha256')
    rights = data['rights']
    user_cls = Users()

    if not email or not name or not password or not rights:
        abort(400)

    is_valid = validate_email(email)
    
    if not is_valid:
        return jsonify({"Alert":"Invalid email adress"}), 200

    if not user_cls.get_user_by_email(email):
        user_cls.add_user(name, email, password, rights)
        return jsonify({"Message": "User '{0}' registered successfully".format(name)}), 201
    
    else:
        return jsonify({"Alert": "Email '{0}' already exists".format(email)}), 200


@userbp.route('/auth/login', methods=['POST'])
def user_login():
        data = request.json

        email = data['email']
        user_password = data['password']

        if not email or not user_password:
            abort(400)

        user_cls = Users()

        logged_user = user_cls.login_user(email)

        if not logged_user:
            return jsonify({"Alert":"Wrong email address"}), 200

        password = check_password_hash(logged_user['password'], user_password)

        if not password:
            return jsonify({"Alert":"Wrong password"}), 200

        access_token = create_access_token(identity=email, expires_delta=timedelta(hours=1))

        return jsonify(access_token=access_token)

@userbp.route('/users', methods=['GET'])
# @jwt_required
def get_all_users():
    user_cls = Users()
    return jsonify({"Users": user_cls.get_all_users()})


@userbp.route('/users/<email>', methods=['GET'])
# @jwt_required
def get_user_by_email(email):
    user_cls = Users()
    user = user_cls.get_user_by_email(email)
    if not user:
        abort(404)
    return jsonify({"User":user})

@userbp.route('/users/<int:user_id>', methods=['GET'])
# @jwt_required
def get_user_by_id(user_id):
    user_cls = Users()    
    user = user_cls.get_user_by_id(user_id)
    if not user:
        abort(404)
    return jsonify({"User":user})

@userbp.route('/users/<email>', methods=['DELETE'])
# @jwt_required
def delete_user(email):
    user_cls = Users()
    user = user_cls.get_user_by_email(email)
    if not user:
        return jsonify({"Not found":"User with email '{0}' not found".format(email)}),404
    user_cls.delete_user_by_email(email)
    return jsonify({"Deleted": "User has been deleted"}), 202

# @userbp.route('/logout')
# @jwt_required
# def logout():
#     session.pop('logged_in', None)
#     return jsonify({"Message": "You have logged out"})
