import json
from os import path

from constants import CONFIG_PATH, DEFAULT_CONFIG_PATH


class SettingsModel:
    def __init__(self):
        with open(DEFAULT_CONFIG_PATH, "r") as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                setattr(self, key, value)

        if path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as json_file:
                data = json.load(json_file)
                for key, value in data.items():
                    setattr(self, key, value)

    def update_setting(self, new_value):
        self.setting_value = new_value

    # iterate through all the object vars and return false if any are default
    def validate_nondefault(self):
        with open(DEFAULT_CONFIG_PATH, "r") as json_file:
            default = json.load(json_file)
            for key, value in vars(self).items():
                if default[key] == value:
                    return False
        return True

