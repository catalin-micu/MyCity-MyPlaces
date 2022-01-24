from datetime import datetime
import googlemaps

from googlemaps_api import get_city_point

gmaps = googlemaps.Client(key='AIzaSyBZ7l2jGuWaRGn2rm1TKhW3GjmraDCpEgA')

if __name__ == '__main__':
    print('rotodendron')
    geo = gmaps.geocode('craiova')
    # directions = gmaps.directions('Focsani, fratiei 3', 'Craiova, 1 decembrie 1918 23', mode='transit',
    #                               departure_time=datetime.now())
    place_id = gmaps.find_place(input=['la rocca'], input_type='textquery', location_bias=get_city_point('craiova'))
    place_id = place_id['candidates'][0]['place_id']
    place = gmaps.place(place_id)
    a=2
