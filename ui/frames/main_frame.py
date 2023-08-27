from customtkinter import CTkFrame, CTkTabview


class MainFrame(CTkFrame):
    def __init__(self, master, bot_controller, settings_controller):
        super().__init__(master, corner_radius=0, fg_color="transparent")

        self.bot_controller = bot_controller
        self.settings_controller = settings_controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create tabview
        self.tabview = CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)