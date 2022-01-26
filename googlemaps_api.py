import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBZ7l2jGuWaRGn2rm1TKhW3GjmraDCpEgA')


def get_city_point(city: str) -> str:
    """
    formats coordinates for city
    :param city: desired city for geolocation
    :return: formatted coordinates according to point:lat,lng
    """
    geo = gmaps.geocode(city)[0]
    if 'locality' not in geo['types']:
        raise ValueError(f'Cannot find given city "{city}"')
    coordinates = geo['geometry']['location']

    return f'point:{coordinates["lat"]},{coordinates["lng"]}'


def place_search(string_query: str, city: str) -> dict:
    """
    searches for a place in a specific city
    :param string_query: name of the place
    :param city: city in which the place can be found
    :return: full result of googlemaps api search
    """
    place_id = gmaps.find_place(input=[string_query], input_type='textquery', location_bias=get_city_point(city))
    place_id = place_id['candidates'][0]['place_id']

    return gmaps.place(place_id)['result']


def place_search_using_gmaps_id(place_ids: []) -> []:
    result = []
    for id in place_ids:
        gmaps_data = gmaps.place(id)['result']
        result.append({
            'name': gmaps_data.get('name'),
            'rating': gmaps_data.get('rating')
        })

    return result


def get_place_coordinates(place_id: str) -> dict:
    coordinates = gmaps.place(place_id)['result']

    return coordinates['geometry']['location']
