from flask import jsonify, request, abort, Blueprint, session
from api.views.functions import Users, users
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

userbp = Blueprint('userbp', __name__)


# Login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({"Unauthorized":"You need to login first"})

        return wrap


@userbp.route('/signup', methods=['POST'])
def register_user():
    data = request.json

    email = data['email']
    name = data['name']
    password = generate_password_hash(data['password'], method='sha256')
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


@userbp.route('/login', methods=['POST', 'GET'])
def user_login():
    
    if request.method == 'POST':
        data = request.json

        email = data['email']
        password = data['password']

        if not email or not password:
            abort(400)

        user = [user for user in users if user['email'] == email]

        if len(user) == 0:
            return jsonify({"Failure": "Wrong login information"}), 200

        compare_password = check_password_hash(user[0]['password'], password)

        if compare_password is True:
            session['logged_in'] = True
            return jsonify({"Success": "User Logged in successfuly"}), 200

        elif compare_password is False:
            return jsonify({"Failure": "Wrong login information"}), 200

@userbp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({"Message": "You have logged out"})

@userbp.route('/users', methods=['GET'])
def get_all_users():
    return jsonify({"Users": users})


@userbp.route('/users/<email>', methods=['GET'])
def get_user_by_id(email):
    user = [user for user in users if email in user.values()]
    if len(user) == 0:
        return jsonify({"Not Found": "No user with email '{0}' in the database".format(email)}), 404

    else:
        return jsonify({"User": user}), 200


@userbp.route('/users/<email>', methods=['DELETE'])
def delete_user(email):
    user = [user for user in users if user['email'] == email]
    if len(user) < 1:
        return jsonify({"Alert": "User with email '{0}' not in the list".format(email)}), 404

    else:
        users.remove(user[0])
        return jsonify({"Deleted": "User '{0}' has been deleted".format(user[0]['name'])}), 200
