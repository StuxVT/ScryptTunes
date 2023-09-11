import tkinter as tk

from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton
from ui.controllers.bot_controller import BotController
from ui.controllers.settings_controller import SettingsController


class Sidebar(CTkFrame):
    def __init__(self, master, bot_controller: BotController, settings_controller: SettingsController, title: str):
        super().__init__(master, corner_radius=0, width=180)

        self.bot_controller = bot_controller
        self.settings_controller = settings_controller

        self.logo_label = CTkLabel(self, text=title, font=CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.start_button = CTkButton(self, text="Start", command=self.handle_start_button)
        self.start_button.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.stop_button = CTkButton(self, text="Stop", command=self.handle_stop_button, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=0, padx=20, pady=(20, 10))

        self.settings_button = CTkButton(self, text="Settings", command=settings_controller.show_settings_window)
        self.settings_button.grid(row=3, column=0, padx=20, pady=(20, 10))

    def handle_start_button(self):
        # todo: don't disable on fail to start
        self.bot_controller.start()
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

    def handle_stop_button(self):
        # todo: don't disable on fail to stop
        self.bot_controller.stop()
        self.stop_button.configure(state=tk.DISABLED)
        self.start_button.configure(state=tk.NORMAL)
