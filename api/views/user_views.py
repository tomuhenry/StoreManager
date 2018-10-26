from flask import Flask, jsonify, json, request, abort, Blueprint
from api.views.functions import Users, users

userbp = Blueprint('userbp',__name__)

@userbp.route('/signup', methods=['POST'])
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
        return jsonify({"Error": "Invalid email"}), 200

    if user_cls.check_duplicate() is False:
        return jsonify({"Failed": "User with email '{0}' already exists".format(email)}), 200

    user_cls.add_user()
    return jsonify({"Success": "User with name '{0}' has been added".format(name)}), 200


@userbp.route('/login', methods=['POST'])
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


@userbp.route('/users', methods=['GET'])
def get_all_users():
    return jsonify({"Users": users})


@userbp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = [user for user in users if user_id in user.values()]
    if len(user) == 0:
        return jsonify({"Not Found": "No user with ID '{0}' in the database".format(user_id)}), 404

    else:
        return jsonify({"User": user}), 200

@userbp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = [user for user in users if user['user_id'] == user_id]
    if len(user) < 1:
        return jsonify({"Alert": "User with ID '{0}' not in the list".format(user_id)}), 404

    else:
        users.remove(user[0])
        return jsonify({"Deleted": "User '{0}' has been deleted".format(user[0]['name'])}), 200
