from customtkinter import CTkFrame, CTkEntry, CTkButton

from ui.frames.list_input import ListInput

class SettingsFrame(CTkFrame):
    def __init__(self, master, settings_controller):
        super().__init__(master)

        self.settings_controller = settings_controller

        self.setting_entry = CTkEntry(self)
        self.setting_entry.insert(0, settings_controller.get("nickname"))
        self.save_button = CTkButton(self, text="Save", command=self.save_setting)

        self.list_entry = ListInput(self)

        self.setting_entry.pack()
        self.save_button.pack()
        self.list_entry.pack()


    def save_setting(self):
        new_value = self.setting_entry.get()
        self.settings_controller.update_setting(new_value)

