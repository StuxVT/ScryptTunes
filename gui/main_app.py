import tkinter

import tkinter as tk
from gui.screens.home_screen import HomeScreen
# from gui.screens.settings_screen import SettingsScreen

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Tkinter App")

        self.home_screen = HomeScreen(self.root)
        # self.settings_screen = SettingsScreen(self.root)

        # Configure menu
        self.menu = tkinter.Menu()
        self.menu.add_command(label="Home", command=self.show_home_screen)
        # self.menu.add_command(label="Settings", command=self.show_settings_screen)

        # Show initial screen
        self.show_home_screen()

    def show_home_screen(self):
        self.hide_all_screens()
        self.home_screen.show()

    # def show_settings_screen(self):
    #     self.hide_all_screens()
    #     self.settings_screen.show()

    def hide_all_screens(self):
        self.home_screen.hide()
        # self.settings_screen.hide()
