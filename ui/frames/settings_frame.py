from customtkinter import CTkFrame, CTkButton

from ui.frames.list_setting_row import ListSettingRow
from ui.frames.text_setting_row import TextSettingRow


class SettingsFrame(CTkFrame):
    def __init__(self, master, settings_controller):
        super().__init__(master)

        self.settings_controller = settings_controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Configure row 0 to expand vertically

        # Nickname
        self.nickname_row = TextSettingRow(self, setting_name="Nickname",
                                           setting_description="idk what this does",
                                           initial_value=settings_controller.get("nickname"))
        self.nickname_row.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Prefix
        self.prefix_row = TextSettingRow(self, setting_name="Prefix",
                                         setting_description="Indicates a chat command for this bot",
                                         initial_value=settings_controller.get("prefix"))
        self.prefix_row.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Channels
        self.channels_row = ListSettingRow(self, setting_name="Channels",
                                           setting_description="idk what this does",
                                           initial_value=settings_controller.get("channels"))
        self.channels_row.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Token
        self.token_row = TextSettingRow(self, setting_name="Token",
                                        setting_description="sum kinda token",
                                        initial_value=settings_controller.get("token"),
                                        hidden=True)
        self.token_row.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Client Id
        self.client_id_row = TextSettingRow(self, setting_name="client_id",
                                            setting_description="sum kinda token",
                                            initial_value=settings_controller.get("client_id"),
                                            hidden=True)
        self.client_id_row.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # client_secret
        self.client_secret = TextSettingRow(self, setting_name="client_secret",
                                            setting_description="sum kinda token",
                                            initial_value=settings_controller.get("client_secret"),
                                            hidden=True)
        self.client_secret.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # channel_points_reward
        self.channel_points_reward = TextSettingRow(self, setting_name="channel_points_reward",
                                                    setting_description="sum kinda token",
                                                    initial_value=settings_controller.get("channel_points_reward"))
        self.channel_points_reward.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        # spotify_client_id
        self.spotify_client_id = TextSettingRow(self, setting_name="spotify_client_id",
                                                setting_description="sum kinda token",
                                                initial_value=settings_controller.get("spotify_client_id"),
                                                hidden=True)
        self.spotify_client_id.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

        # spotify_secret
        self.spotify_secret = TextSettingRow(self, setting_name="spotify_secret",
                                             setting_description="sum kinda token",
                                             initial_value=settings_controller.get("spotify_secret"),
                                             hidden=True)
        self.spotify_secret.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

        # spotify_redirect_uri
        self.spotify_redirect_uri = TextSettingRow(self, setting_name="spotify_redirect_uri",
                                                   setting_description="sum kinda token",
                                                   initial_value=settings_controller.get("spotify_redirect_uri"),
                                                   hidden=True)
        self.spotify_redirect_uri.grid(row=9, column=0, padx=10, pady=5, sticky="ew")

        # Save Settings
        self.save_button = CTkButton(self, text="Save", command=self.save_settings)
        self.save_button.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def save_settings(self):
        self.settings_controller.set('nickname', self.nickname_row.get())
        self.settings_controller.set('prefix', self.prefix_row.get())
        self.settings_controller.set('channels', self.channels_row.get())
        self.settings_controller.set('token', self.token_row.get())
        self.settings_controller.set('client_id', self.client_id_row.get())
        self.settings_controller.set('client_secret', self.client_secret.get())
        self.settings_controller.set('channel_points_reward', self.channel_points_reward.get())
        self.settings_controller.set('spotify_client_id', self.spotify_client_id.get())
        self.settings_controller.set('spotify_secret', self.spotify_secret.get())
        self.settings_controller.set('spotify_redirect_uri', self.spotify_redirect_uri.get())

        self.settings_controller.save_config()
