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
