from flask import jsonify, request, abort, Blueprint
from api.models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (get_raw_jwt, jwt_required,
                                create_access_token, get_jwt_identity)
from validate_email import validate_email
from datetime import timedelta

userbp = Blueprint('userbp', __name__)

user_cls = Users()


def user_check():
    current_user = get_jwt_identity()
    user = user_cls.get_user_by_email(current_user)
    if user['rights'] == True:
        return True
    else:
        return False


@userbp.route('/auth/signup', methods=['POST'])
@jwt_required
def register_user():
    data = request.json

    email = data['email']
    name = data['name']
    password = generate_password_hash(data['password'], method='sha256')
    rights = bool(data['rights'])

    if not email or not name or not password:
        abort(400)

    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to add user"}), 401

    is_valid = validate_email(email)

    if not is_valid:
        return jsonify({"Alert": "Invalid email address"}), 200

    if not user_cls.get_user_by_email(email):
        user_cls.add_user(name, email, password, rights)
        return jsonify({"Message": "User '{0}' registered successfully".format(name)}), 201
    return jsonify({"Alert": "Email '{0}' already exists".format(email)}), 200


@userbp.route('/auth/login', methods=['POST'])
def user_login():
    data = request.json

    email = data['email']
    user_password = data['password']

    if not email or not user_password:
        abort(400)

    logged_user = user_cls.login_user(email)

    if not logged_user:
        return jsonify({"Alert": "Wrong email address"}), 200

    password = check_password_hash(logged_user['password'], user_password)

    if not password:
        return jsonify({"Alert": "Wrong password"}), 200

    access_token = create_access_token(
        identity=email, expires_delta=timedelta(days=1))

    if logged_user['rights'] == True:
        return jsonify({"admin_token": access_token})
    return jsonify({"user_token": access_token})


@userbp.route('/users', methods=['GET'])
@jwt_required
def get_all_users():
    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to perform action"}), 401
    all_users = user_cls.get_all_users()
    return jsonify(all_users)


@userbp.route('/users/<email>', methods=['GET'])
@jwt_required
def get_user_by_email(email):
    user = user_cls.get_user_by_email(email)
    if not user:
        return jsonify({"Not Found": "No user with email '{0}'".format(email)}), 404
    return jsonify(user)


@userbp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user_by_id(user_id):
    user = user_cls.get_user_by_id(user_id)
    if not user_check():
        return jsonify({"Alert": "You don't have permission for this action"}), 401
    if not user:
        abort(404)
    return jsonify(user)


@userbp.route('/users/<email>', methods=['DELETE'])
@jwt_required
def delete_user(email):
    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to perform action"})
    user = user_cls.get_user_by_email(email)
    if not user:
        return jsonify({"Not found": "User with email '{0}' not found".format(email)}), 404
    user_cls.delete_user_by_email(email)
    return jsonify({"Deleted": "User has been deleted"}), 202


@userbp.route('/users/<user_id>', methods=['PUT'])
@jwt_required
def edit_user(user_id):
    data = request.json
    rights = data['rights']

    if user_check() is False:
        return jsonify({"Alert": "You're not Authorized to perform action"})

    user = user_cls.get_user_by_id(user_id)
    if not user:
        return jsonify({"Not found": "User with ID '{0}' not found".format(user_id)}), 404

    user_cls.edit_user_rights(user_id, rights)
    return jsonify({"Modified": "User Rights have been changed"}), 200


@userbp.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    user_cls.add_token(jti)
    return jsonify({"Bye": "You have logged out successfully"}), 200
