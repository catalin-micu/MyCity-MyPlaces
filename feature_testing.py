import json
from googlemaps_api import get_city_point, place_search
from models.families import Families
from models.family_members import FamilyMembers
from models.places import Places
from models.users import Users
from utils import user_batch_insert

if __name__ == '__main__':
    # user_batch_insert('data_files/users.json')

    users = Users()
    # users.get_user_data('catalinmicu98@gmail.com', 'email')

    families = Families()
    # fam_data = ["Ale Micu", "The Bornacs", "Potopurile"]
    # for item in fam_data:
    #     families.insert_family(item)

    family_members = FamilyMembers()
    # family_members.insert_family_member(family_id=3, user_id=2)

    places = Places()
    with open('data_files/places.json') as f:
        input_json = json.load(f)
    # places.delete_place('1', 'place_id')
    # places.insert_place(input_json[0])

    x = place_search('electroputere mall', 'craiova')
    a=2
