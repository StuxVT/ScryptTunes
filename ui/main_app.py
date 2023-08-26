# global
import tkinter as tk

# local
from ui.controllers.bot_controller import BotController
from ui.controllers.settings_controller import SettingsController
from ui.models.bot_model import BotModel
from ui.models.settings_model import SettingsModel
from ui.views.main_view import MainView


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Tkinter App")

        #Init MVCs
        self.bot_model = BotModel()
        self.settings_model = SettingsModel()

        self.bot_controller = BotController(self.bot_model)
        self.settings_controller = SettingsController(self.settings_model)

        self.home_screen = MainView(self.root, self.bot_controller, self.settings_controller)

        # Configure menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.submenu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Menu", menu=self.submenu)
        self.submenu.add_command(label="Settings", command=self.show_settings_screen)

        # Show initial screen
        self.home_screen.show()

    def show_settings_screen(self):
        pass
