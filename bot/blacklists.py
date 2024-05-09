# todo: add separate functionality for each blacklist types
# global
import json

# local
from constants import USER_BLACKLIST, SONG_BLACKLIST


def read_json(filename):
    if filename == "blacklist":
        file = SONG_BLACKLIST
    else:
        file = USER_BLACKLIST

    with open(file, "r") as f:
        data = json.load(f)
    return data


def write_json(data, filename):
    if filename == "blacklist":
        file = SONG_BLACKLIST
    else:
        file = USER_BLACKLIST

    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def is_blacklisted(user_name):
    """
    Reads blacklist file, creates list of blacklisted users, iterates list looking for user.

        TODO: this is super inefficient. Does not need to be O(n)
            - shouldn't have to read and rebuild list on EVERY request
            - instead, store a hashmap
    :param user_name:
    :return: bool:
    """

    return user_name.lower() in read_json("blacklist_user")["users"]
