import customtkinter as ctk
import json
from os import path

import constants
from ui.models.song_blacklist import SongBlacklist
from ui.models.user_blacklist import UserBlacklist
from ui.models.config import Config
from ui.views.settings_view import SettingsView


class SettingsController:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.default = False

        # ensure song blacklist exists
        if path.exists(constants.SONG_BLACKLIST_PATH):
            with open(constants.SONG_BLACKLIST_PATH) as config:
                self.blacklist_model = SongBlacklist(**json.load(config))
        else:
            self.song_blacklist = SongBlacklist()
            self.save_song_blacklist()

        # ensure user blacklist exists
        if path.exists(constants.USER_BLACKLIST_PATH):
            with open(constants.USER_BLACKLIST_PATH) as config:
                self.user_blacklist = UserBlacklist(**json.load(config))
        else:
            self.user_blacklist = UserBlacklist()
            self.save_user_blacklist()

        # load settings here if they exist, else default and mark as default
        if path.exists(constants.CONFIG_PATH):
            with open(constants.CONFIG_PATH) as config:
                self.config_model = Config(**json.load(config))
        else:
            self.config_model = Config()
            self.save_config()

    def get(self, key):
        # todo, validate and handle errors
        return getattr(self.config_model, key)

    def set(self, key, value):
        # todo, validate and handle errors
        setattr(self.config_model, key, value)
        return True

    def save_config(self):
        with open(constants.CONFIG_PATH, "w") as json_file:
            json.dump(self.config_model.model_dump(), json_file, indent=4)

    def save_user_blacklist(self):
        with open(constants.USER_BLACKLIST_PATH, "w") as json_file:
            json.dump(self.user_blacklist.model_dump(), json_file, indent=4)

    def save_song_blacklist(self):
        with open(constants.SONG_BLACKLIST_PATH, "w") as json_file:
            json.dump(self.song_blacklist.model_dump(), json_file, indent=4)

    def show_settings_window(self):
        x_offset, y_offset = map(int, self.root.geometry().split('+')[1:3])
        SettingsView(self, geometry=f"{800}x{600}+{x_offset}+{y_offset}").grab_set()  # grab focus until closed
