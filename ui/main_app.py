# global
import customtkinter as ctk

# local
from ui.controllers.bot_controller import BotController
from ui.controllers.settings_controller import SettingsController
from ui.models.bot_model import BotModel
from ui.models.settings_model import SettingsModel
from ui.views.main_view import MainView

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ScryptTunes")
        self.geometry(f"{800}x{500}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #Init MVCs
        self.bot_model = BotModel()
        self.settings_model = SettingsModel()

        self.bot_controller = BotController(self.bot_model)
        self.settings_controller = SettingsController(self.settings_model)

        MainView(self, self.bot_controller, self.settings_controller).show()
