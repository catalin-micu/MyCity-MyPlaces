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
    place_id = gmaps.find_place(input=[string_query], input_type='textquery', location_bias=get_city_point(city))
    place_id = place_id['candidates'][0]['place_id']

    return gmaps.place(place_id)['result']
