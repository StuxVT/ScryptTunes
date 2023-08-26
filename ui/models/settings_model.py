class SettingsModel:
    def __init__(self):
        self.setting_value = "default"

    def update_setting(self, new_value):
        self.setting_value = new_value
