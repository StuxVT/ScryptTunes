from customtkinter import CTkFrame, CTkButton

from ui.frames.checkbox_setting_row import CheckboxSettingRow
from ui.frames.text_setting_row import TextSettingRow


class PermissionSettingsFrame(CTkFrame):
    def __init__(self, master, settings_controller):
        super().__init__(master)

        self.settings_controller = settings_controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Configure row 0 to expand vertically

        # Bot account
        self.nickname_row = TextSettingRow(self, setting_name="Bot Account",
                                           setting_description="The username of your bot account",
                                           initial_value=settings_controller.get("nickname"))
        self.nickname_row.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    def save_settings(self):
        self.settings_controller.set('nickname', self.nickname_row.get())

        self.settings_controller.save_config()
