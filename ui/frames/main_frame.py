from customtkinter import CTkFrame, CTkButton


class MainFrame(CTkFrame):
    def __init__(self, master, bot_controller, settings_controller):
        super().__init__(master)

        self.bot_controller = bot_controller
        self.settings_controller = settings_controller

        self.bot_toggle_button = CTkButton(self, text="Toggle Bot", command=self.bot_controller.toggle_bot)

        self.bot_toggle_button.pack()
