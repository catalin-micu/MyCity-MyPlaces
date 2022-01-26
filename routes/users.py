from flask import jsonify, Blueprint, request, Response
from models.users import Users

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')
users = Users()


@users_blueprint.route('/create-user', methods=['POST'])
def create_user():
    """
    {
        "user_name": "Micu Marius Catalin",
        "address_line": "Sergent Ilie Petre 86",
        "city": "Chiajna",
        "email": "catalinmicu98@gmail.com",
        "passwd": "password"
    }
    """
    data = request.json
    users.insert_user(data)

    return Response(f"Successfully created user for email '{data.get('email')}'", status=200)


@users_blueprint.route('/get-user-info', methods=['POST'])
def get_user_info():
    """
    {
        "email": "catalinmicu98@gmail.com"
    }
    """
    email = request.json.get('email')
    if not email:
        return Response('Email must be present in request body', status=400)
    used_data = users.get_user_data(email, 'email')

    return jsonify(used_data)


@users_blueprint.route('/login', methods=['POST'])
def login():
    """
    check params
    if params ok, create session_table entry, allow access
    else deny access
    request = dict with two keys: email, passwd
    :return: allow = 200, deny = 403
    """
    data = request.json
    email = data.get('email')
    passwd = data.get('passwd')

    if users.check_login_credentials(email, passwd):
        return Response('All good', status=200)
    else:
        return Response('Invalid credentials! Access denied', status=403)
