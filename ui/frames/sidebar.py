from customtkinter import CTkFrame, CTkLabel, CTkFont


class Sidebar(CTkFrame):
    def __init__(self, master, bot_controller, settings_controller, title):
        super().__init__(master, corner_radius=0, width=180)

        self.bot_controller = bot_controller
        self.settings_controller = settings_controller

        self.logo_label = CTkLabel(self, text=title, font=CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

