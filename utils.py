import json

from models.users import Users


def user_batch_insert(file_path: str):
    users = Users()

    with open(file_path) as f:
        input_json = json.load(f)

    for item in input_json:
        users.insert_user(item)


def calculate_average(input_list: list) -> float:
    return sum(input_list) / len(input_list)
