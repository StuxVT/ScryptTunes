from ui.models.settings_model import SettingsModel
from ui.views.settings_view import SettingsView


class SettingsController:
    def __init__(self):
        # load settings here if they exist, else default and mark as default
        self.settings_model = SettingsModel()
        self.default = True

    def get(self, key):
        # todo, validate and handle errors
        getattr(self.settings_model, key)
        return True

    def set(self, key, value):
        # todo, validate and handle errors
        setattr(self.settings_model, key, value)
        return True

    def show_settings_window(self):
        SettingsView(self).grab_set()  # grab focus until closed
