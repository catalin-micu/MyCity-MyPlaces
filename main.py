from datetime import datetime
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBZ7l2jGuWaRGn2rm1TKhW3GjmraDCpEgA')

if __name__ == '__main__':
    print('rotodendron')
    # geo = gmaps.geocode('86 Sergent Ilie Petre')
    # directions = gmaps.directions('Focsani, fratiei 3', 'Craiova, 1 decembrie 1918 23', mode='transit',
    #                               departure_time=datetime.now())
    place_id = gmaps.find_place(input=['la rocca'], input_type='textquery', location_bias='point:44.33,27.79')
    place_id = place_id['candidates'][0]['place_id']
    place = gmaps.place(place_id)
    a=2
