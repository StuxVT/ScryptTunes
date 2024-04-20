import json

# Third Party
from pydantic import ValidationError

# Local
from constants import CONFIG
from ui.models.config import Config

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
