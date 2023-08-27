import customtkinter as ctk
import tkinter as tk
from ui.views.settings_view import SettingsView


class SettingsController:
    def __init__(self, settings_model):
        self.settings_model = settings_model

    def update_setting(self, new_value):
        self.settings_model.update_setting(new_value)

    def show_settings(self):
        SettingsView(self).grab_set()  # grab focus until closed
