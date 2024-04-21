from customtkinter import CTkFrame

from ui.frames.permission_setting_row import PermissionSettingRow
from bot.scrypt_tunes import Bot


class PermissionSettingsFrame(CTkFrame):
    def __init__(self, master, settings_controller):
        """
        TODO: dead settings can be created if command names change, find workaround or fix/autoclean somehow

        :param master:
        :param settings_controller:
        """

        super().__init__(master)

        self.settings_controller = settings_controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Configure row 0 to expand vertically

        #
        self.ping_command_setting = PermissionSettingRow(
            parent=self,
            setting_name="Ping Command",
            setting_description="Change permissions on the ping command",
            initial_values=None,  # todo: get from existing config
            command_name="ping_command"  # todo: reference command in non-hardcoded way
        )
        self.ping_command_setting.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    def save_settings(self):
        # todo

        # self.settings_controller.set('nickname', self.ping_command_setting.get())
        #
        # self.settings_controller.save_config()
        pass
