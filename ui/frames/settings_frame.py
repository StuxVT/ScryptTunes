from customtkinter import CTkFrame, CTkEntry, CTkButton

from ui.frames.list_input import ListInput
from ui.frames.setting_row import SettingRow


class SettingsFrame(CTkFrame):
    def __init__(self, master, settings_controller):
        super().__init__(master)

        self.settings_controller = settings_controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Nickname (occupies row 0 and 1)
        self.nickname_input = CTkEntry(self)
        self.nickname_input.insert(0, settings_controller.get("nickname"))
        self.nickname_row = SettingRow(self, setting_name="Nickname", setting_description="idk what this does",
                                       input_widget=self.nickname_input)
        self.nickname_row.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Save Settings
        self.save_button = CTkButton(self, text="Save", command=self.save_settings)
        self.save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # # Channels
        # self.list_entry = ListInput(self)
        #

    def save_settings(self):
        self.settings_controller.set('nickname', self.nickname_input.get())

        self.settings_controller.save_settings()
