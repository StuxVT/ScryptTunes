import tkinter as tk
from ui.frames.settings_frame import SettingsFrame

class SettingsView:
    def __init__(self, root, settings_controller):
        self.settings_frame = SettingsFrame(root, settings_controller)

    def show(self):
        self.settings_frame.pack()
