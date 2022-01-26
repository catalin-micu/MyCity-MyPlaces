from flask import jsonify, Blueprint, request, Response
from googlemaps_api import place_search, place_search_using_gmaps_id, get_place_coordinates
from models.families import Families
from models.family_members import FamilyMembers
from models.places import Places
from models.users import Users
from utils import calculate_average

places_blueprint = Blueprint('places_blueprint', __name__, url_prefix='/places')
places = Places()
users = Users()
families = Families()
family_members = FamilyMembers()


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


@places_blueprint.route('/add-place', methods=['POST'])
def add_place():
    string_query = request.json.get('string_query')
    city = request.json.get('city')
    if not string_query or not city:
        return Response("Invalid request body", status=400)
    # to be continued
    # will not not continue


@places_blueprint.route('/place-ratings', methods=['POST'])
def get_place_ratings_for_user():
    result = []
    email = request.json.get('email')
    if not email:
        return Response("email not in request body", status=400)
    user_id = users.get_user_data(identifier=email, identifier_type='email').get('user_id')
    favourite_places = places.get_places(identifier=user_id, identifier_type='user_id')
    favourite_places = [item['google_id'] for item in favourite_places]
    raw_places_data = place_search_using_gmaps_id(favourite_places)

    place_ratings = {
        'key': 'Places ratings',
        'values': [{'x': item['name'], 'y': item['rating']} for item in raw_places_data]
    }
    result.append(place_ratings)
    rating_avg = [float(item['rating']) for item in raw_places_data]
    rating_avg = calculate_average(rating_avg)

    average_rating = {
        'key': 'Average rating',
        'values': [{'x': item['name'], 'y': rating_avg} for item in raw_places_data]
    }
    result.append(average_rating)

    return jsonify(result)


@places_blueprint.route('/family-places', methods=['POST'])
def get_family_places():
    result = []
    email = request.json.get('email')
    if not email:
        return Response("email not in request body", status=400)

    user_id = users.get_user_data(identifier=email, identifier_type='email').get('user_id')
    family_members_ids = family_members.get_family_members_of_user(user_id)
    for id in family_members_ids:
        rows = places.get_places(identifier=id, identifier_type='user_id')
        non_private_places = []
        for r in rows:
            if r['is_private'] == False:
                non_private_places.append({
                    'google_id': r['google_id'],
                    'user_id': r['user_id']
                })
        for item in non_private_places:
            result.append(item)

    true_result = []
    for item in result:
        coordinates = get_place_coordinates(item['google_id'])
        coordinates['user_id'] = item['user_id']
        true_result.append(coordinates)

    return jsonify(true_result)


@places_blueprint.route('/popularity', methods=['GET'])
def compute_places_popularity():
    places_ids = places.get_all_google_ids()
    occurences = []
    for id in places_ids:
        occurences.append({
            'x': place_search_using_gmaps_id([id])[0]['name'],
            'y': len(places.get_places(identifier=id, identifier_type='google_id'))
        })

    return jsonify([{
        'key': 'Places popularity',
        'values': occurences
    }])
