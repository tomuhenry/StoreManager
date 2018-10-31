from flask import jsonify, request, abort, Blueprint, session, Flask
from api.models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (jwt_required, create_access_token,
    get_jwt_identity)
from validate_email import validate_email
from datetime import timedelta

userbp = Blueprint('userbp', __name__)


@userbp.route('/signup', methods=['POST'])
# @jwt_required
def register_user():
    data = request.json

    email = data['email']
    name = data['name']
    password = generate_password_hash(data['password'], method='sha256')
    rights = bool(data['rights'])

    if not email or not name or not password or not rights:
        abort(400)

    is_valid = validate_email(email)
    if not is_valid:
        return jsonify({"Alert":"Invalid email adress"})

    new_user = Users()
    try:
        new_user.add_user(name, email, password, rights)
        return jsonify({
            "message": "User '{0}' registered successfully".format(name)
        }), 201

    except:
        return jsonify({"message": "Unable to register user"}), 500


@userbp.route('/login', methods=['POST'])
def user_login():
        data = request.json

        email = data['email']
        user_password = data['password']
        
        logged_user = Users()

        if not email or not user_password:
            abort(400)

        get_user = logged_user.login_user(email)

        if not get_user:
            return jsonify({"Alert":"Wrong email adress"})

        password = check_password_hash(get_user['password'], user_password)

        if not password:
            return jsonify({"Alert":"Wrong password"})

        access_token = create_access_token(identity=email, expires_delta=timedelta(hours=1))

        return jsonify(access_token=access_token)

# @userbp.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     return jsonify({"Message": "You have logged out"})

# @userbp.route('/users', methods=['GET'])
# def get_all_users():
#     return jsonify({"Users": users})


# @userbp.route('/users/<email>', methods=['GET'])
# def get_user_by_id(email):
#     user = [user for user in users if email in user.values()]
#     if len(user) == 0:
#         return jsonify({"Not Found": "No user with email '{0}' in the database".format(email)}), 404

#     else:
#         return jsonify({"User": user}), 200


# @userbp.route('/users/<email>', methods=['DELETE'])
# def delete_user(email):
#     user = [user for user in users if user['email'] == email]
#     if len(user) < 1:
#         return jsonify({"Alert": "User with email '{0}' not in the list".format(email)}), 404

#     else:
#         users.remove(user[0])
#         return jsonify({"Deleted": "User '{0}' has been deleted".format(user[0]['name'])}), 200
