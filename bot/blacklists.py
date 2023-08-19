import json
import os

def read_json(filename):
    with open(f"config/{filename}.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"config/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)

def is_blacklisted(user_name):
    '''
    Reads blacklist file, creates list of blacklisted users, iterates list looking for user.

        TODO: this is super inefficient. Does not need to be O(n)
            - shouldn't have to read and rebuild list on EVERY request
            - instead, store a hashmap
    :param user_name:
    :return: bool:
    '''

    return user_name.lower() in read_json("blacklist_user")["users"]
