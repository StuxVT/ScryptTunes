from typing import List

from customtkinter import CTkFrame, CTkButton

from ui.frames.permission_setting_row import PermissionSettingRow
from ui.models.config import PermissionSetting, PermissionSettingDict, PermissionConfig


class PermissionSettingsFrame(CTkFrame):
    def __init__(self, master, settings_controller):
        """
        TODO: dead settings can be created if command names change, find workaround or fix/autoclean somehow

        :param master:
        :param settings_controller:
        """

        super().__init__(master)

        self.settings_controller = settings_controller
        self.current_settings = settings_controller.get("permissions")  # type: PermissionSettingDict

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Configure row 0 to expand vertically

        #
        self.ping_command_setting = PermissionSettingRow(
            parent=self,
            setting_name="Ping Command",
            setting_description="Change permissions on the ping command",
            initial_values=self.current_settings.ping_command.permission_config,
            command_name="ping_command"  # todo: reference command in non-hardcoded way
        )
        self.ping_command_setting.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Save Settings
        self.save_button = CTkButton(self, text="Save", command=self.save_settings)
        self.save_button.grid(
            row=11, column=0, columnspan=2, padx=10, pady=5, sticky="ew"
        )

    def save_settings(self):
        new_settings = {
            "ping_command": self.ping_command_setting.get()
        }

        self.settings_controller.set('permissions', PermissionSettingDict(**new_settings))
        self.settings_controller.save_config()

