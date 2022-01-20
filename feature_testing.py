from models.families import Families
from models.family_members import FamilyMembers
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
    family_members.insert_family_members(1, 2)
    a=2
