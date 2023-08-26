from customtkinter import CTkFrame, CTkEntry, CTkButton


class SettingsFrame(CTkFrame):
    def __init__(self, master, settings_controller):
        super().__init__(master)

        self.settings_controller = settings_controller

        self.setting_entry = CTkEntry(self)
        self.save_button = CTkButton(self, text="Save", command=self.save_setting)

        self.setting_entry.pack()
        self.save_button.pack()

    def save_setting(self):
        new_value = self.setting_entry.get()
        self.settings_controller.update_setting(new_value)
