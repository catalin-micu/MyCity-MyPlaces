from flask import jsonify, Blueprint, request, Response

from googlemaps_api import place_search
from models.users import Users

places_blueprint = Blueprint('places_blueprint', __name__, url_prefix='/places')


@places_blueprint.route('/search-place', methods=['POST'])
def search_place():
    """
    {
        "string_query": "<value>",
        "city": "<value>"
    }
    :return: response obj
    """
    string_query = request.json.get('string_query')
    city = request.json.get('city')
    if not string_query or not city:
        return Response("Invalid request body", status=400)

    return jsonify(place_search(string_query, city))
