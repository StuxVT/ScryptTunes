import customtkinter as ctk
import json
from os import path

from ui.models.settings_model import SettingsModel
from ui.views.settings_view import SettingsView
from constants import CONFIG_PATH


class SettingsController:
    def __init__(self, root: ctk.CTk):
        self.root = root

        # load settings here if they exist, else default and mark as default
        if path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as config:
                self.settings_model = SettingsModel(**json.load(config))
        else:
            self.settings_model = SettingsModel()
            self.default = True

    def get(self, key):
        # todo, validate and handle errors
        return getattr(self.settings_model, key)

    def set(self, key, value):
        # todo, validate and handle errors
        setattr(self.settings_model, key, value)
        return True

    def show_settings_window(self):
        x_offset, y_offset = map(int, self.root.geometry().split('+')[1:3])
        SettingsView(self, geometry=f"{400}x{200}+{x_offset}+{y_offset}").grab_set()  # grab focus until closed