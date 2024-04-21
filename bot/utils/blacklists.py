# global
import json

# local
from constants import USER_BLACKLIST, SONG_BLACKLIST

# todo: add separate functionality for each blacklist types


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


def is_user_blacklisted(username: str) -> bool:
    '''
     Reads blacklist file, creates list of blacklisted users, iterates list looking for user.

         TODO: this is super inefficient. Does not need to be O(n)
             - shouldn't have to read and rebuild list on EVERY request
             - instead, store a hashmap
     :param username: the username to check
     :return: bool:
     '''
    if username is None:
        # This is a failsafe, if a username is not provided assume its blacklisted (just to be safe)
        return True

    return username.lower() in read_json("blacklist_user")["users"]


def is_song_blacklisted(song_id: str) -> bool:
    if song_id is None:
        # This is a failsafe, if a song is not provided assume its blacklisted (just to be safe)
        return True

    return song_id in read_json("blacklist")["blacklist"]


def blacklist_user(username: str) -> bool:
    """
    Adds a username to blacklist
    Args:
        username: the username to add

    Returns: True if the user was added, False if the user was already blacklisted
    """
    user = username.lower()
    file = read_json("blacklist_user")
    if user in file["users"]:
        return False

    file["users"].append(user)
    write_json(file, "blacklist_user")
    return True


def unblacklist_user(username: str) -> bool:
    """
    Removes a username to blacklist
    Args:
        username: the username to remove

    Returns: True if the user was removed, False if the user was not blacklisted in the first place
    """
    user = username.lower()
    file = read_json("blacklist_user")
    if user not in file["users"]:
        return False

    file["users"].remove(user)
    write_json(file, "blacklist_user")
    return True


def blacklist_song(song_uri: str) -> bool:
    """
        Adds a song to blacklist
        Args:
            song_uri: the song uri to add

        Returns: True if the song was added, False if the song was already blacklisted
        """
    file = read_json("blacklist")
    if song_uri in file["blacklist"]:
        return False
    file["blacklist"].append(song_uri)
    write_json(file, "blacklist")
    return True


def unblacklist_song(song_uri: str) -> bool:
    """
    Removes a song from the blacklist
    Args:
        song_uri: the song to remove

    Returns: True if the song was removed, False if the song was not blacklisted in the first place
    """
    file = read_json("blacklist")
    if song_uri not in file["blacklist"]:
        return False

    file["blacklist"].remove(song_uri)
    write_json(file, "blacklist")
    return True
