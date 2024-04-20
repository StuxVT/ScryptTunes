import json
import os
import logging

from pydantic import ValidationError

from constants import CONFIG
from ui.models.config import Config


def get_bot_version() -> str:
    """
    Returns the version of the bot found in the /VERSION file
    :return: String of the file version
    """
    # todo: I am not really sure if the bundled .exe will contain the VERSION file (and in the same location)
    # If this is not the case then this SHOULD CHANGE!

    # Parent directory of bot module

    dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        print(dir_path)
        with open(os.path.join(dir_path, "VERSION")) as version_file:
            return version_file.read().strip()

    except FileNotFoundError:
        logging.warning("Could not fetch VERSION file")
    return "0.0"


def get_bot_config() -> Config:
    """
    Gets the contents of the config json (this code was directly extracted from the scrypt_tunes.Bot class)
    :return: Config instance of the saved config
    """
    with open(CONFIG) as config_file:
        config_data = json.load(config_file)
    try:
        return Config(**config_data)
    except ValidationError:
        return Config()
