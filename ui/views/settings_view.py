import customtkinter as ctk
from ui.frames.settings_frame import SettingsFrame


class SettingsView(ctk.CTkToplevel):
    def __init__(self, settings_controller, geometry):
        super().__init__()
        self.geometry(geometry) if geometry else self.geometry(f"{400}x{200}")

        self.grid_rowconfigure(0, weight=1)  # Configure row 0 to expand vertically
        self.grid_columnconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid_rowconfigure(0, weight=1)  # Configure row 0 to expand vertically
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")

        self.settings_frame = SettingsFrame(self.scroll_frame, settings_controller)
        self.settings_frame.grid(row=0, column=0, sticky="nsew")

    def show(self):
        self.settings_frame.pack()
