from datetime import datetime
import googlemaps

from googlemaps_api import get_city_point, place_search

gmaps = googlemaps.Client(key='AIzaSyBZ7l2jGuWaRGn2rm1TKhW3GjmraDCpEgA')

if __name__ == '__main__':
    # pppppppp = gmaps.place('ChIJxUvmMpzXUkcRfJzbDwbpiEU')
    p = place_search('english park', 'craiova')
    id = p['place_id']
    a=2
